import os
import tempfile
import unittest

# Use a separate temporary database for tests.
fd, test_db = tempfile.mkstemp()
os.environ["DATABASE_PATH"] = test_db

from app import app, init_db  # noqa: E402


class FindItTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        init_db()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"FindIt", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "healthy")

    def test_report_found_item(self):
        response = self.client.post("/report", data={
            "item_name": "Blue bottle",
            "category": "Other",
            "location": "Library",
            "description": "Blue steel bottle",
            "report_type": "Found",
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Blue bottle", response.data)


if __name__ == "__main__":
    unittest.main()
