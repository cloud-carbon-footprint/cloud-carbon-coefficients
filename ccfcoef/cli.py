import inspect
from pathlib import Path

import click
import pandas as pd

import ccfcoef.constants as const
from ccfcoef.cpu_info import CPUInfo
from ccfcoef.specpower import SPECPower

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR.joinpath('data')

CPU_FAMILIES = ['amd-epyc-gen1',
                'amd-epyc-gen2',
                'amd-epyc-gen3',
                'intel-broadwell',
                'intel-cascadelake',
                'intel-haswell',
                'intel-ivybridge',
                'intel-sandybridge',
                'intel-skylake']


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
        families = [cpu_family]

    spec = SPECPower.instantiate(DATA_DIR.joinpath('SPECpower-full-results.csv'))

    for cpu_family in families:
        cpu_info = CPUInfo.instantiate(DATA_DIR.joinpath(f'{cpu_family}.csv'))
        cpu_power = spec.get_cpu_power(cpu_info)
        click.secho(f'Averages for: {cpu_family}', fg='green')
        display_cpu_power(cpu_power)


def display_cpu_power(cpu_power):
    click.echo(f'Average: Min Watts = {cpu_power.idle_watts():,.2f}')
    click.echo(f'Average: Max Watts = {cpu_power.max_watts():,.2f}')
    click.echo(f'Average: Max Watts (GCP) = {cpu_power.max_watts_gcp_adjusted():,.2f}')
    click.echo(f'Average: GB/chip = {cpu_power.gb_chip():,.2f}')


@cli.command()
def test():
    click.echo('Test!')


if __name__ == '__main__':
    cli()
