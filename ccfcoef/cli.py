import inspect
import sys
from pathlib import Path

import click
import pandas as pd

import ccfcoef.constants as const
from ccfcoef.aws.coefficients import AWSCoefficients
from ccfcoef.azure.coefficients import AzureCoefficients
from ccfcoef.gcp.coefficients import GCPCoefficients
from ccfcoef.cpu_info import CPUInfo
from ccfcoef.cpu_power import CPUPower
from ccfcoef.family import Family
from ccfcoef.specpower import SPECPower

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR.joinpath('data')
OUTPUT_DIR = PROJECT_DIR.joinpath('output')

CPU_FAMILIES = [
    Family(name='EPYC 1st Gen', short='amd-epyc-gen1'),
    Family(name='EPYC 2nd Gen', short='amd-epyc-gen2'),
    Family(name='EPYC 3rd Gen', short='amd-epyc-gen3'),
    Family(name='Sandy Bridge', short='intel-sandybridge'),
    Family(name='Ivy Bridge', short='intel-ivybridge'),
    Family(name='Haswell', short='intel-haswell'),
    Family(name='Broadwell', short='intel-broadwell'),
    Family(name='Skylake', short='intel-skylake'),
    Family(name='Cascade Lake', short='intel-cascadelake'),
    Family(name='Coffee Lake', short='intel-coffeelake')]


@click.group()
def cli():
    pass


@cli.command()
def show_constants():
    """Display all constants available to ccfcoef.
    For details on each constant, see the 'constants.py' file.
    """
    click.secho('Constants in use:', fg='green')
    for name, value in inspect.getmembers(const):
        if name.isupper():
            click.secho(f'{click.style(name, fg="white")} = {click.style(value, fg="yellow")}')


@cli.command()
def show_families():
    """Display all CPU families available to ccfcoef.
    These families are stored in the 'data/' directory and contain
    the list of micro-architectures for each family.
    """
    click.secho('CPU families in use:', fg='green')
    for family in CPU_FAMILIES:
        click.secho(f'{click.style(family.name, fg="white")} = {click.style(family.short, fg="yellow")}')


@cli.command()
def cpu_averages():
    """Display the calculated power usage averages for each CPU family."""
    cpus_power = calculate_cpus_families_power(CPU_FAMILIES)
    for name, power in cpus_power.items():
        click.secho(f'Averages for: {name}', fg='green')
        display_cpu_power(power)


@cli.command()
@click.option('-w', '--write', is_flag=True, help='Write the output to a file')
def usage_coefficients(write):
    """Calculate the usage coefficients for each cloud provider."""
    click.secho('Calculating usage coefficients...', fg='cyan')
    output = {True: write_dataframes, False: display_dataframes}

    cpus_power = calculate_cpus_families_power(CPU_FAMILIES)

    click.secho('Azure', fg='green')
    azure = AzureCoefficients.instantiate(DATA_DIR.joinpath('azure-instances.csv'))
    coefficients = to_dataframe(azure.use_coefficients(cpus_power))
    output[write](coefficients, 'coefficients-azure-use.csv')

    click.secho('GCP', fg='green')
    gcp = GCPCoefficients.instantiate(DATA_DIR.joinpath('gcp-instances.csv'))
    coefficients = to_dataframe(gcp.use_coefficients(cpus_power))
    output[write](coefficients, 'coefficients-gcp-use.csv')

    click.secho('AWS', fg='green')
    aws = AWSCoefficients.instantiate(DATA_DIR.joinpath('aws-instances.csv'))
    coefficients = to_dataframe(aws.use_coefficients(cpus_power))
    output[write](coefficients, 'coefficients-aws-use.csv')


@cli.command()
@click.option('-w', '--write', is_flag=True, help='Write the output to a file')
def embodied_coefficients(write):
    """Calculate the embodied coefficients for each cloud provider."""
    click.secho('Calculating embodied coefficients...', fg='cyan')
    output = {True: write_dataframes, False: display_dataframes}

    gcp_cpus = pd.read_csv(DATA_DIR.joinpath('gcp-instances-cpus.csv'))
    aws_cpus = pd.read_csv(DATA_DIR.joinpath('aws-instances-cpus.csv'))

    click.secho('Azure', fg='green')
    azure = AzureCoefficients.instantiate(DATA_DIR.joinpath('azure-instances.csv'))
    # Azure uses GCP CPUs for embodied coefficients, the original comments about was:
    # 'For Azure & GCP we only know the general CPU architecture'
    output[write](to_dataframe(azure.embodied_coefficients(gcp_cpus)), 'coefficients-azure-embodied.csv')

    click.secho('GCP', fg='green')
    gcp = GCPCoefficients.instantiate(DATA_DIR.joinpath('gcp-instances.csv'))
    gcp_embodied_coefficients_df = to_dataframe(gcp.embodied_coefficients(gcp_cpus))
    output[write](gcp_embodied_coefficients_df, 'coefficients-gcp-embodied.csv')

    click.secho('GCP (mean)', fg='green')
    output[write](to_dataframe(gcp.embodied_coefficients_mean(gcp_embodied_coefficients_df)),
                  'coefficients-gcp-embodied-mean.csv')

    click.secho('AWS', fg='green')
    aws = AWSCoefficients.instantiate(DATA_DIR.joinpath('aws-instances.csv'))
    output[write](to_dataframe(aws.embodied_coefficients(aws_cpus)), 'coefficients-aws-embodied.csv')


def display_dataframes(df, filename=None):
    click.echo(df)


def write_dataframes(df, filename):
    output_file = OUTPUT_DIR.joinpath(filename)
    click.secho(f'Writing to {output_file.relative_to(OUTPUT_DIR.parent)}, {len(df)} entries.', fg='white')
    df.to_csv(output_file)


def to_dataframe(coefficients):
    coefficients = pd.DataFrame(coefficients)
    coefficients = coefficients.drop_duplicates(ignore_index=True)
    return coefficients


def calculate_cpus_families_power(families):
    spec = SPECPower.instantiate(DATA_DIR.joinpath('SPECpower-full-results.csv'))
    cpus_power = {}
    for cpu_family in families:
        cpu_info = CPUInfo.instantiate(DATA_DIR.joinpath(f'{cpu_family.short}.csv'))
        spec_power = spec.get_cpu_power(cpu_info)

        cpus_power[cpu_family.name] = CPUPower(
            min_watts=spec_power.idle_watts(),
            max_watts=spec_power.max_watts(),
            max_watts_gcp_adjusted=spec_power.max_watts_gcp_adjusted(),
            gb_chip=spec_power.gb_chip(),
            cpu_info=cpu_info
        )

    return cpus_power


def display_cpu_power(cpu_power):
    click.echo(f'Average: Min Watts = {cpu_power.min_watts:,.2f}')
    click.echo(f'Average: Max Watts = {cpu_power.max_watts:,.2f}')
    click.echo(f'Average: Max Watts (GCP) = {cpu_power.max_watts_gcp_adjusted:,.2f}')
    click.echo(f'Average: GB/chip = {cpu_power.gb_chip:,.2f}')


if __name__ == '__main__':
    cli()
