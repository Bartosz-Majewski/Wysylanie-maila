"""Context manager for email sender"""
import smtplib
import ssl
from collections import namedtuple

Credentials = namedtuple('Credentials', 'username password')


class EmailSender:
    def __init__(self, port, smtp_server, credentials, ssl_enabled=False):
        self.port = port
        self.smtp_server = smtp_server
        self.ssl_enabled = ssl_enabled
        self.connection = None
        self.credentials = credentials

    def __enter__(self):
        if not self.ssl_enabled:
            self.connection = smtplib.SMTP(self.smtp_server, self.port)
        else:
            context = ssl.create_default_context()
            self.connection = smtplib.SMTP_SSL(
                self.smtp_server, self.port, context)

        self.connection.login(self.credentials.username,
                              self.credentials.password)

        return self

    def sendmail(self, sender, receiver, message):
        self.connection.sendmail(sender, receiver, message.as_string())

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.connection.close()
