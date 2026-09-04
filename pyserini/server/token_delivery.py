#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Out-of-band delivery for pre-generated Pyserini API tokens."""

from __future__ import annotations

import smtplib
import ssl
import stat
from email.message import EmailMessage
from pathlib import Path
from typing import Protocol


class TokenEmailSender(Protocol):
    def send(self, *, name: str, email: str, token: str) -> None:
        """Deliver one token without returning or logging it."""


class SmtpTokenEmailSender:
    """Send a token through TLS SMTP, optionally using SMTP authentication."""

    DEFAULT_STARTTLS_PORT = 587
    DEFAULT_TIMEOUT_SEC = 20.0
    FORBIDDEN_CC_DOMAINS = frozenset({'googlegroups.com'})
    VALID_SECURITY_MODES = frozenset({'starttls', 'ssl'})

    __slots__ = (
        '_host',
        '_port',
        '_sender',
        '_cc',
        '_username',
        '_password',
        '_security',
        '_timeout_sec',
    )

    def __init__(
        self,
        *,
        host: str,
        port: int,
        sender: str,
        cc: tuple[str, ...],
        username: str | None = None,
        password_file: str | None = None,
        security: str = 'starttls',
        timeout_sec: float = DEFAULT_TIMEOUT_SEC,
    ) -> None:
        self._host = host.strip() if isinstance(host, str) else ''
        self._sender = sender.strip() if isinstance(sender, str) else ''
        self._cc = tuple(address.strip() for address in cc if address.strip())
        self._username = username.strip() if isinstance(username, str) and username.strip() else None
        self._security = security.strip().casefold() if isinstance(security, str) else ''
        self._port = int(port)
        self._timeout_sec = float(timeout_sec)
        if not self._host:
            raise ValueError('SMTP host is required')
        if self._port <= 0 or self._port > 65535:
            raise ValueError('SMTP port must be in [1, 65535]')
        if not self._sender:
            raise ValueError('Token email sender address is required')
        if not self._cc:
            raise ValueError('At least one token email CC address is required')
        if any(
            address.rsplit('@', 1)[-1].casefold() in self.FORBIDDEN_CC_DOMAINS
            for address in self._cc
        ):
            raise ValueError('Token email CC addresses must be individual mailboxes, not Google Groups')
        if self._security not in self.VALID_SECURITY_MODES:
            raise ValueError(f'SMTP security must be one of {sorted(self.VALID_SECURITY_MODES)}')
        if self._timeout_sec <= 0:
            raise ValueError('SMTP timeout must be positive')
        if bool(self._username) != bool(password_file):
            raise ValueError('SMTP username and password file must be configured together')

        self._password = None
        if password_file:
            path = Path(password_file).expanduser().resolve()
            if not path.is_file():
                raise ValueError(f'SMTP password file not found: {path}')
            if stat.S_IMODE(path.stat().st_mode) & 0o077:
                raise ValueError('SMTP password file must not be accessible by group or other users')
            password = path.read_text(encoding='utf-8').strip()
            if not password:
                raise ValueError('SMTP password file is empty')
            self._password = password

    def _message(self, *, name: str, email: str, token: str) -> EmailMessage:
        message = EmailMessage()
        message['Subject'] = 'Your Pyserini REST API token'
        message['From'] = self._sender
        message['To'] = email
        message['Cc'] = ', '.join(self._cc)
        message.set_content(
            f'Hello {name},\n\n'
            'Your Pyserini REST API token is:\n\n'
            f'{token}\n\n'
            'Keep this credential private and send it only in an Authorization header. '
            'This token is issued once for the lifetime of this email address.\n\n'
            'This is a no-reply email. To contact the service administrators, use Reply all and '
            "ask the administrators who are CC'd on this message.\n"
        )
        return message

    def send(self, *, name: str, email: str, token: str) -> None:
        message = self._message(name=name, email=email, token=token)
        recipients = [email, *self._cc]
        context = ssl.create_default_context()
        if self._security == 'ssl':
            with smtplib.SMTP_SSL(
                self._host,
                self._port,
                timeout=self._timeout_sec,
                context=context,
            ) as smtp:
                if self._username:
                    smtp.login(self._username, self._password)
                smtp.send_message(message, from_addr=self._sender, to_addrs=recipients)
            return

        with smtplib.SMTP(self._host, self._port, timeout=self._timeout_sec) as smtp:
            smtp.ehlo()
            smtp.starttls(context=context)
            smtp.ehlo()
            if self._username:
                smtp.login(self._username, self._password)
            smtp.send_message(message, from_addr=self._sender, to_addrs=recipients)
