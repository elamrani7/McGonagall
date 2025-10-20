import unittest
from app.gui import heure_range

class TestGuiUtils(unittest.TestCase):
    def test_heure_range_basic(self):
        result = heure_range("09:00", "12:00")
        self.assertEqual(result, ["09:00", "10:00", "11:00"])

    def test_heure_range_empty(self):
        result = heure_range("09:00", "09:00")
        self.assertEqual(result, [])
