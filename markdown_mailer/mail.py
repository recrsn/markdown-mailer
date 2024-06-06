import os
from collections.abc import Iterable
from dataclasses import dataclass
from dataclasses import field
from typing import cast

import frontmatter


@dataclass
class Mail:
    body: str
    from_: str
    to: Iterable[str]
    subject: str | None = None
    cc: Iterable[str] = field(default_factory=list)
    bcc: Iterable[str] = field(default_factory=list)
    body_format: str = 'html'
    attachments: Iterable[str] = field(default_factory=list)


def _listify(value: str | Iterable[str]) -> Iterable[str]:
    if value is None:
        return []
    elif isinstance(value, str):
        return [value]
    else:
        return value


def _resolve_attachments(attachments: Iterable[str], base_dir: str) -> Iterable[str]:
    return [os.path.join(base_dir, attachment) for attachment in attachments]


def parse_mail(content: str, attachment_base: str) -> Mail:
    """
    Parse a markdown email file into a Mail object.
    :param content:
    :param attachment_base:
    """
    email_file = frontmatter.loads(content)
    metadata = email_file.metadata

    return Mail(
        body=email_file.content,
        from_=cast(str, metadata['from']),
        to=_listify(cast(str | Iterable[str], metadata['to'])),
        subject=cast(str | None, metadata.get('subject')),
        cc=_listify(cast(str | Iterable[str] | None, metadata.get('cc'))),
        bcc=_listify(cast(str | Iterable[str] | None, metadata.get('bcc'))),
        attachments=_resolve_attachments(cast(list[str], metadata.pop('attachments', [])), attachment_base)
    )
