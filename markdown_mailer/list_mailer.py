from jinja2 import Environment
from jinja2 import FileSystemLoader

from markdown_mailer.connection import Connection
from markdown_mailer.mail import parse_mail
from markdown_mailer.mailer import send_mail


def send_list_mail(connection: Connection, context: list[dict[str, str]], template: str, base_dir: str) -> None:
    """
    Send an email to a list of recipients using a markdown template.

    Args:
        connection: The connection details for the SMTP server.
        context: A list of dictionaries containing the context for each email.
        template: The path to the markdown template file.
        base_dir: The base directory for resolving attachments.

    Returns:
        None
    """

    environment = Environment(loader=FileSystemLoader(base_dir))
    template = environment.get_template(template)

    for email_context in context:
        email = parse_mail(template.render(**email_context), base_dir)
        send_mail(connection, email)
