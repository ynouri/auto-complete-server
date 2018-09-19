"""Start and test the web server."""

import json
from tornado.testing import AsyncHTTPTestCase
from auto_complete_server.web import app


class TestAutoCompleteServer(AsyncHTTPTestCase):
    """Test the auto-complete server."""

    def get_app(self):
        """Create the web application."""
        return app.make_app()

    def test_autocomplete(self):
        """Test the auto-complete REST API."""
        response = self.fetch("/autocomplete?q=H")
        test_json = json.loads(response.body)
        expected_json = {
            "completions": [
                "How can I help you?",
                "Have a great day Wernzio",
                "Hello Werner how may I help you today?",
            ]
        }
        self.assertEqual(response.code, 200)
        self.assertEqual(test_json, expected_json)

    def test_autocomplete_with_space(self):
        """Test auto-complete with a space in the prefix."""
        response = self.fetch("/autocomplete?q=How+can")
        test_json = json.loads(response.body)
        expected_json = {"completions": ["How can I help you?"]}
        self.assertEqual(response.code, 200)
        self.assertEqual(test_json, expected_json)

    def test_autocomplete_no_prefix(self):
        """Test auto-complete request without prefix."""
        response = self.fetch("/autocomplete")
        self.assertEqual(response.code, 400)

    def test_autocomplete_empty_prefix(self):
        """Test auto-complete request with an empty prefix."""
        response = self.fetch("/autocomplete?q=")
        test_json = json.loads(response.body)
        expected_json = {"completions": []}
        self.assertEqual(response.code, 200)
        self.assertEqual(test_json, expected_json)
