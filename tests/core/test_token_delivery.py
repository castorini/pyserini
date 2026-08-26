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

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from pyserini.server.token_delivery import SmtpTokenEmailSender


class TestSmtpTokenEmailSender(unittest.TestCase):
    def test_starttls_delivery_sends_to_user_and_cc(self):
        with tempfile.TemporaryDirectory() as tmp:
            password_path = Path(tmp) / 'smtp-password'
            password_path.write_text('secret-password\n', encoding='utf-8')
            password_path.chmod(0o600)
            sender = SmtpTokenEmailSender(
                host='smtp.example.edu',
                port=587,
                sender='tokens@example.edu',
                cc=('audit@example.edu',),
                username='smtp-user',
                password_file=str(password_path),
            )
            smtp = MagicMock()
            smtp.__enter__.return_value = smtp
            with patch('pyserini.server.token_delivery.smtplib.SMTP', return_value=smtp):
                sender.send(
                    name='Test User',
                    email='user@example.edu',
                    token='a' * 64,
                )

            smtp.starttls.assert_called_once()
            smtp.login.assert_called_once_with('smtp-user', 'secret-password')
            message = smtp.send_message.call_args.args[0]
            self.assertEqual(message['To'], 'user@example.edu')
            self.assertEqual(message['Cc'], 'audit@example.edu')
            self.assertIn('a' * 64, message.get_content())
            self.assertEqual(
                smtp.send_message.call_args.kwargs['to_addrs'],
                ['user@example.edu', 'audit@example.edu'],
            )

    def test_password_file_must_be_private(self):
        with tempfile.TemporaryDirectory() as tmp:
            password_path = Path(tmp) / 'smtp-password'
            password_path.write_text('secret-password\n', encoding='utf-8')
            password_path.chmod(0o644)
            with self.assertRaisesRegex(ValueError, 'group or other'):
                SmtpTokenEmailSender(
                    host='smtp.example.edu',
                    port=587,
                    sender='tokens@example.edu',
                    cc=('audit@example.edu',),
                    username='smtp-user',
                    password_file=str(password_path),
                )
            self.assertEqual(os.stat(password_path).st_mode & 0o777, 0o644)

    def test_username_and_password_file_are_configured_together(self):
        with self.assertRaisesRegex(ValueError, 'configured together'):
            SmtpTokenEmailSender(
                host='smtp.example.edu',
                port=587,
                sender='tokens@example.edu',
                cc=('audit@example.edu',),
                username='smtp-user',
            )

    def test_google_group_cannot_receive_token_cc(self):
        with self.assertRaisesRegex(ValueError, 'individual mailboxes'):
            SmtpTokenEmailSender(
                host='smtp.example.edu',
                port=587,
                sender='tokens@example.edu',
                cc=('research-list@googlegroups.com',),
            )


if __name__ == '__main__':
    unittest.main()
