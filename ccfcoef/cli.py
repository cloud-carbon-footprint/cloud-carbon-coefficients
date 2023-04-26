import pprint
from pathlib import Path

import click
import inspect
import pandas as pd

import ccfcoef.constants as const
from ccfcoef import cpu_info
from ccfcoef.cpu_info import CPUInfo
from ccfcoef.servers import Servers

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR.joinpath('data')


@click.group()
def cli():
    pass


@cli.command()
def constants():
    c_list = []
    click.secho('Constants in use:', fg='green')
    for name, value in inspect.getmembers(const):
        if name.isupper():
            click.secho(f'{click.style(name, fg="white")} = {click.style(value, fg="yellow")}')


@cli.command()
def generate():
    click.echo('generating data')
    svs = pd.read_csv(DATA_DIR.joinpath('SPECpower-full-results.csv'), na_values=['NC'])
    servers = Servers(svs)
    click.echo(servers)


@cli.command()
@click.argument('cpu_family')
def average(cpu_family):
    family_file = DATA_DIR.joinpath(f'{cpu_family}.csv')
    if not family_file.exists():
        click.secho(f'No data for {cpu_family}', fg='red')
        return
    cpus = cpu_info.load_append_list(family_file)
    cpu = CPUInfo(cpus)
    servers = Servers.instantiate(DATA_DIR.joinpath('SPECpower-full-results.csv'), cpu.cpu_re)

    click.echo(f'Average: Min Watts = {servers.idle_watts():,.2f}')
    click.echo(f'Average: Max Watts = {servers.max_watts():,.2f}')
    click.echo(f'Average: Max Watts (GCP) = {servers.max_watts_gcp_adjusted():,.2f}')
    click.echo(f'Average: GB/chip = {servers.gb_chip():,.2f}')



@cli.command()
def test():
    click.echo('Test!')


if __name__ == '__main__':
    cli()
