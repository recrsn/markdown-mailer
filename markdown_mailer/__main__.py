import csv
import os

import click
import yaml

from markdown_mailer import mailer
from markdown_mailer.connection import parse_connection
from markdown_mailer.list_mailer import send_list_mail
from markdown_mailer.mail import parse_mail


@click.group
def cli() -> None:
    """
    Markdown Mailer

    A command line tool to send emails using markdown files.
    """
    pass


def _load_connections(config: click.File):
    with config:
        mail_config = yaml.load(config, Loader=yaml.SafeLoader)
        connections = {
            name: parse_connection(name, params)
            for name, params in mail_config['connections'].items()
        }
    return connections


@cli.command()
@click.option('--config', type=click.File('r'), default='mailer.yml')
@click.option('--connection', type=str, default='default')
@click.argument('mail', type=click.File('r'))
def send(mail: click.File, config: click.File, connection: str):
    """
    Send an email
    """
    connections = _load_connections(config)

    with mail as f:
        email = parse_mail(f.read(), os.path.dirname(mail.name))
        mailer.send_mail(connections[connection], email)


@cli.command()
@click.option('--config', type=click.File('r'), default='mailer.yml')
@click.option('--connection', type=str, default='default')
@click.argument('template', type=click.File('r'))
@click.argument('context', type=click.File('r'))
def send_list(connection: str, config: click.File, template: str, context: click.File):
    """
    Send an email to a list of recipients
    """
    connections = _load_connections(config)

    template_name = os.path.basename(template)
    base_dir = os.path.dirname(template)

    with context as f:
        reader = csv.DictReader(f)
        context = list(reader)

    send_list_mail(connections[connection], context, template_name, base_dir)


if __name__ == '__main__':
    cli()
