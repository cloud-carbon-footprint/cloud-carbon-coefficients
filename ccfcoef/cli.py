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
@click.option('-f', '--family', default='all', help='CPU family to display, ex: intel-skylake')
def cpu_average(family):
    """List the average power consumption of CPUs in a family."""
    if family == 'all':
        families = CPU_FAMILIES
    else:
        # find which family by its short name
        families = [f for f in CPU_FAMILIES if f.short == family]
    # handle invalid family selection
    if len(families) == 0:
        click.secho(f'Family "{family}" not found in CPU_FAMILIES, use "ccfcoef show-families" to list them.', fg='red')
        sys.exit(1)

    cpus_power = calculate_cpus_families_power(families)
    for name, power in cpus_power.items():
        click.secho(f'Averages for: {name}', fg='green')
        display_cpu_power(power)


@cli.command()
def usage_coefficients():
    cpus_power = calculate_cpus_families_power(CPU_FAMILIES)

    click.secho('Azure', fg='green')
    azure = AzureCoefficients.instantiate(DATA_DIR.joinpath('azure-instances.csv'))
    coefficients = to_unique_dataframe(azure.use_coefficients(cpus_power))
    click.echo(coefficients)

    click.secho('GCP', fg='green')
    gcp = GCPCoefficients.instantiate(DATA_DIR.joinpath('gcp-instances.csv'))
    coefficients = to_unique_dataframe(gcp.use_coefficients(cpus_power))
    click.echo(coefficients)

    click.secho('AWS', fg='green')
    aws = AWSCoefficients.instantiate(DATA_DIR.joinpath('aws-instances.csv'))
    coefficients = to_unique_dataframe(aws.use_coefficients(cpus_power))
    click.echo(coefficients)


@cli.command()
def embodied_coefficients():
    gcp_cpus = pd.read_csv(DATA_DIR.joinpath('gcp-instances-cpus.csv'))
    aws_cpus = pd.read_csv(DATA_DIR.joinpath('aws-instances-cpus.csv'))

    click.secho('Azure', fg='green')
    azure = AzureCoefficients.instantiate(DATA_DIR.joinpath('azure-instances.csv'))
    click.echo(to_unique_dataframe(azure.embodied_coefficients(gcp_cpus)))
    click.secho('GCP', fg='green')
    gcp = GCPCoefficients.instantiate(DATA_DIR.joinpath('gcp-instances.csv'))
    click.echo(to_unique_dataframe(gcp.embodied_coefficients(gcp_cpus)))


def to_unique_dataframe(coefficients):
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
