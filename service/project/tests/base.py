"""Base setup for all test."""

from flask_testing import TestCase  # type: ignore

from project import create_app

app = create_app()


class BaseTestCase(TestCase):
    """Creates app and subclasses inherit app."""

    def create_app(self):
        return app
