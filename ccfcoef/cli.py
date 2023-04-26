from pathlib import Path

import click
import inspect
import pandas as pd

import ccfcoef.constants as const
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
def test():
    click.echo('Test!')


if __name__ == '__main__':
    cli()
