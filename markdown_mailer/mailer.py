import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Iterable

import markdown


def send_mail(connection: dict,
              body: str,
              from_: str,
              to: str | Iterable[str],
              subject: str | None = None,
              cc: str | Iterable[str] | None = None,
              bcc: str | Iterable[str] | None = None,
              body_format: str = 'html',
              attachments: Iterable[str] = None
              ):
    if isinstance(to, str):
        to = [to]

    if isinstance(cc, str):
        cc = [cc]
    elif cc is None:
        cc = []

    if isinstance(bcc, str):
        bcc = [bcc]
    elif bcc is None:
        bcc = []

    if attachments is None:
        attachments = []

    recipients = to + cc + bcc

    msg = MIMEMultipart('alternative')
    msg['From'] = from_
    msg['To'] = ', '.join(to)

    if subject:
        msg['Subject'] = subject

    if cc:
        msg['Cc'] = ', '.join(cc)

    if body_format == 'plain':
        msg.attach(MIMEText(body, 'plain'))
    else:
        msg.attach(MIMEText(markdown.markdown(body), 'html'))

    for attachment in attachments:
        with open(attachment, 'rb') as f:
            part = MIMEApplication(f.read())
            file_name = os.path.basename(f.name)
            part.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(part)

    with smtplib.SMTP(connection['smtp_server'], connection['smtp_port']) as server:
        server.starttls()
        server.login(connection['smtp_user'], connection['smtp_password'])
        server.send_message(msg, from_addr=from_, to_addrs=recipients)

        print('Email sent successfully!')
