# Markdown Mailer

A simple module to send markdown emails using the `smtplib` module in Python.

## Features

- Send markdown emails
- Send emails with attachments
- Send emails with inline images
- Full CC and BCC support
- Send emails with multiple recipients
- Send customized emails to a list using templates and CSV files

## How to use

### Generate a configuration file

Check `mailer.yml.example` for an example configuration file. You can copy it
into `mailer.yml` and fill in the SMTP server details. You can also specify
multiple configurations and choose which one to use when sending an email.

### Send a simple email

With the configuration file in place, you can send a simple email by creating a
Markdown file with front matter and the email content.

```markdown
---
from: User Name <user@example.com>
to: Recipient Name <receipient@example.com>
cc:
  - CC Name <cc@example.com>
subject: Subject of the email
attachments:
  - support_files/attachment.pdf
---

Hello, World!

This is the body of the email. You can use markdown here.

This is a new paragraph.

- You can also use lists
- Like this one

You can also use **bold** and *italic* text.

You can also use [links](https://example.com).

You can also use inline code like `print("Hello, World!")`.

You can use simple HTML tags like <br> to add line breaks.

This is the end of the email.<br>
Thanks!
```

You can then send this email using the following command:

```bash
python -m markdown_mailer send emails/test_email.md
```

### Send a templated email to multiple recipients using a CSV file

You can also send customized emails to multiple recipients using a template and a
CSV file. The CSV file should have columns with the same names as the variables
used in the template.

Anything can be a variable in the template, including the subject, body, and
attachments. The template can be a markdown file with front matter or a plain
text file. We use the [Jinja2 templating engine](https://jinja.palletsprojects.com/)
to render the template.

```markdown
---
From: User Name <user@example.org>
To: {{ first_name }} {{ last_name }} <{{ email }}>
Subject: Welcome to our platform, {{ first_name }}!
Attachments:
  - support_files/welcome.pdf
---

Hello, {{ first_name }}!

Welcome to our platform. We are excited to have you on board.

Please find attached a welcome document that explains how to get started.

If you have any questions, feel free to reach out to your dedicated account manager,
{{ account_manager }} at {{ account_manager_email }}.

We look forward to working with you.

Best regards,
User Name
```

The CSV file should look like this:

```csv
first_name,last_name,email,account_manager,account_manager_email
Alice,Smith,alice@example.com,Bob Johnson,bob@acme.example.com
Charlie,Brown,charlie@example.com,Dave Williams,dave@acme.example.com
```

You can then send this email using the following command:

```bash
python -m markdown_mailer send-list emails/template_email.md emails/recipients.csv
```
