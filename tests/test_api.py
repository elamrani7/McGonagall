import unittest
from unittest.mock import patch
from app.wigor_api import fetch_schedule
from unittest.mock import patch
from app.wigor_api import fetch_schedule
import unittest

class TestWigorAPI(unittest.TestCase):
    @patch("app.wigor_api.requests.get")
    def test_fetch_schedule_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<html>...</html>"  # Simulé
        result = fetch_schedule("fake_cookie")
        self.assertIsInstance(result, list)

     
    @patch("app.wigor_api.requests.get")
    def test_fetch_schedule_failure(self, mock_get):
        mock_get.return_value.status_code = 403
        with self.assertRaises(Exception):
            fetch_schedule("invalid_cookie")

    @patch("app.wigor_api.requests.get")
    def test_fetch_schedule_error(self, mock_get):
        mock_get.return_value.status_code = 403
        mock_get.return_value.text = "Accès refusé"
        with self.assertRaises(Exception):
            fetch_schedule("invalid_cookie")


    @patch("app.wigor_api.requests.get")
    def test_fetch_schedule_empty_html(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = ""
        result = fetch_schedule("valid_cookie")
        self.assertEqual(result, [])
    
