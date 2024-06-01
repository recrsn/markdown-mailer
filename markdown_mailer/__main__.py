import os
from typing import cast
from typing import Iterable

import click
import frontmatter
import yaml

from markdown_mailer import mailer


@click.group
def cli() -> None:
    """
    Markdown Mailer

    A command line tool to send emails using markdown files.
    """
    pass


def resolve_attachments(attachments: Iterable[str], email_file: str) -> Iterable[str]:
    email_path = os.path.dirname(email_file)
    return [os.path.join(email_path, attachment) for attachment in attachments]


@cli.command()
@click.option('--config', type=click.File('r'), default='mailer.yml')
@click.option('--connection', type=str, default='default')
@click.argument('mail', type=click.File('r'))
def send(mail: click.File, config: click.File, connection: str):
    """
    Send an email
    """
    with config:
        mail_config = yaml.load(config, Loader=yaml.SafeLoader)
        conn = mail_config['connections'][connection]

    with mail as f:
        email_file = frontmatter.load(f)
        metadata = email_file.metadata
        from_ = cast(str, metadata['from'])
        attachments = resolve_attachments(cast(list[str], metadata.pop('attachments', [])), mail.name)
        mailer.send_mail(connection=conn,
                         body=email_file.content,
                         from_=from_,
                         attachments=attachments,
                         **metadata)


if __name__ == '__main__':
    cli()
