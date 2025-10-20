import unittest
from app.config import get_headers, API_URL, API_BASE_URL, TIMEOUT

class TestConfig(unittest.TestCase):
    def test_get_headers_with_cookie(self):
        """Test de la fonction get_headers avec un cookie"""
        cookie = "test_session_123"
        headers = get_headers(cookie)
        
        self.assertIn("Cookie", headers)
        self.assertIn("Accept", headers)
        self.assertEqual(headers["Cookie"], "session=test_session_123")
        self.assertEqual(headers["Accept"], "application/json")

    def test_get_headers_with_empty_cookie(self):
        """Test de la fonction get_headers avec un cookie vide"""
        cookie = ""
        headers = get_headers(cookie)
        
        self.assertIn("Cookie", headers)
        self.assertEqual(headers["Cookie"], "session=")

    def test_get_headers_with_none_cookie(self):
        """Test de la fonction get_headers avec un cookie None"""
        cookie = None
        headers = get_headers(cookie)
        
        self.assertIn("Cookie", headers)
        self.assertEqual(headers["Cookie"], "session=None")

    def test_constants_values(self):
        """Test des constantes de configuration"""
        self.assertEqual(API_URL, "https://wigorservices/api/schedule")
        self.assertEqual(API_BASE_URL, "https://api.wigorservices.net/")
        self.assertEqual(TIMEOUT, 10)

    def test_headers_structure(self):
        """Test de la structure des headers retournés"""
        headers = get_headers("test")
        
        self.assertIsInstance(headers, dict)
        self.assertEqual(len(headers), 2)
        self.assertIn("Cookie", headers)
        self.assertIn("Accept", headers)
