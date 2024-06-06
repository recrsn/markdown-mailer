import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import markdown

from markdown_mailer.connection import Connection
from markdown_mailer.mail import Mail


def send_mail(connection: Connection, mail: Mail) -> None:
    """
    Send an email using the provided connection details and mail object.
    :param connection:
    :param mail:
    """
    to = set(mail.to)
    cc = set(mail.cc)
    bcc = set(mail.bcc)

    recipients = list(to.union(cc).union(bcc))

    msg = MIMEMultipart('alternative')
    msg['From'] = mail.from_
    msg['To'] = ', '.join(to)

    if mail.subject:
        msg['Subject'] = mail.subject

    if cc:
        msg['Cc'] = ', '.join(cc)

    if mail.body_format == 'plain':
        msg.attach(MIMEText(mail.body, 'plain'))
    else:
        msg.attach(MIMEText(markdown.markdown(mail.body), 'html'))

    for attachment in mail.attachments:
        with open(attachment, 'rb') as f:
            part = MIMEApplication(f.read())
            file_name = os.path.basename(f.name)
            part.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(part)

    with smtplib.SMTP(connection.server, connection.port) as server:
        server.starttls()
        server.login(connection.user, connection.password)
        server.send_message(msg, from_addr=mail.from_, to_addrs=recipients)

        print('Email sent successfully!')
