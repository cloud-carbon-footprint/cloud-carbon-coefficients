import inspect
from pathlib import Path

import click
import pandas as pd

import ccfcoef.constants as const
from ccfcoef.azure.coefficients import AzureCoefficients
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
def constants():
    click.secho('Constants in use:', fg='green')
    for name, value in inspect.getmembers(const):
        if name.isupper():
            click.secho(f'{click.style(name, fg="white")} = {click.style(value, fg="yellow")}')


@cli.command()
def generate():
    click.echo('generating data')
    svs = pd.read_csv(DATA_DIR.joinpath('SPECpower-full-results.csv'), na_values=['NC'])
    servers = SPECPower(svs)
    click.echo(servers)


@cli.command()
@click.option('-f', '--cpu-family', default='all', help='CPU family to display')
def average(cpu_family):
    if cpu_family == 'all':
        families = CPU_FAMILIES
    else:
        # find which family by its short name
        families = [f for f in CPU_FAMILIES if f.short == cpu_family]

    cpus_power = calculate_cpus_families_power(families)
    for name, power in cpus_power.items():
        click.secho(f'Averages for: {name}', fg='green')
        display_cpu_power(power)


@cli.command()
def usage_coefficients():
    cpus_power = calculate_cpus_families_power(CPU_FAMILIES)

    azure = AzureCoefficients.instantiate(DATA_DIR.joinpath('azure-instances.csv'))

    coefficients = to_unique_dataframe(azure.create_coefficients(cpus_power))

    click.echo(coefficients)


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
            gb_chip=spec_power.gb_chip())

    return cpus_power


def display_cpu_power(cpu_power):
    click.echo(f'Average: Min Watts = {cpu_power.min_watts:,.2f}')
    click.echo(f'Average: Max Watts = {cpu_power.max_watts:,.2f}')
    click.echo(f'Average: Max Watts (GCP) = {cpu_power.max_watts_gcp_adjusted:,.2f}')
    click.echo(f'Average: GB/chip = {cpu_power.gb_chip:,.2f}')


if __name__ == '__main__':
    cli()
