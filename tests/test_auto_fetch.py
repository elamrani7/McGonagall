import unittest
from unittest.mock import patch
from auto_login import fetch_auto_login, get_cookie_and_hash

class TestAutoLoginErrors(unittest.TestCase):
    @patch("auto_login.get_cookie_and_hash")
    def test_fetch_auto_login_failure(self, mock_func):
        mock_func.side_effect = Exception("hashURL introuvable")
        with self.assertRaises(Exception) as context:
            fetch_auto_login()
        self.assertIn("hashURL", str(context.exception))

    @patch("auto_login.sync_playwright")
    def test_get_cookie_and_hash_mocked(self, mock_playwright):
        mock_browser = mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value
        mock_context = mock_browser.new_context.return_value
        mock_page = mock_context.new_page.return_value

        mock_page.url = "https://wigorservices.net/WebPsDyn.aspx?hashURL=B374EC3DEACC9813449CE1BACB71EFC129841AB8BEB5A9CA07EB53B2EF1B32ED36D176E7F7CC291CF43EE6BE8A7A37EAE66B2425DC6E0019839A9A7AA02D1AEA"
        mock_context.cookies.return_value = [{"name": "session", "value": "xyz"}]

        mock_page.wait_for_selector.return_value = True
        mock_page.fill.return_value = None
        mock_page.click.return_value = None
        mock_page.wait_for_url.return_value = True
        mock_page.content.return_value = ""

        cookie, hash_url = get_cookie_and_hash()
        self.assertIn("session=xyz", cookie)
        self.assertEqual(hash_url, "B374EC3DEACC9813449CE1BACB71EFC129841AB8BEB5A9CA07EB53B2EF1B32ED36D176E7F7CC291CF43EE6BE8A7A37EAE66B2425DC6E0019839A9A7AA02D1AEA")

    @patch("auto_login.get_cookie_and_hash")
    def test_fetch_auto_login_mocked(self, mock_func):
        mock_func.return_value = ("cookie=abc", "HASH123")
        cookie, hash_url = fetch_auto_login()
        self.assertEqual(cookie, "cookie=abc")
        self.assertEqual(hash_url, "HASH123")

    def test_fetch_auto_login_returns_cookie_and_hash(self):
        with patch("auto_login.get_cookie_and_hash") as mock_func:
            mock_func.return_value = ("cookie=abc", "HASH123")
            from auto_login import fetch_auto_login
            cookie, hash_url = fetch_auto_login()
            self.assertEqual(cookie, "cookie=abc")
            self.assertEqual(hash_url, "HASH123")
