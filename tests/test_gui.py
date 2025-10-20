import unittest
from app.gui import heure_range, JOURS, HEURES

class TestGuiLogic(unittest.TestCase):
    def test_course_duration(self):
        heures = heure_range("13:00", "15:00")
        self.assertEqual(len(heures), 2)
        self.assertIn("13:00", heures)
        self.assertIn("14:00", heures)

    def test_heure_range_reverse(self):
        result = heure_range("12:00", "09:00")
        self.assertEqual(result, [])

    def test_heure_range_single_hour(self):
        """Test avec une heure unique"""
        heures = heure_range("10:00", "11:00")
        self.assertEqual(len(heures), 1)
        self.assertIn("10:00", heures)

    def test_heure_range_multiple_hours(self):
        """Test avec plusieurs heures"""
        heures = heure_range("09:00", "12:00")
        self.assertEqual(len(heures), 3)
        self.assertIn("09:00", heures)
        self.assertIn("10:00", heures)
        self.assertIn("11:00", heures)

    def test_heure_range_same_time(self):
        """Test avec la même heure de début et fin"""
        heures = heure_range("14:00", "14:00")
        self.assertEqual(heures, [])

    def test_heure_range_edge_cases(self):
        """Test des cas limites"""
        # Test avec des heures en fin de journée
        heures = heure_range("17:00", "18:00")
        self.assertEqual(len(heures), 1)
        self.assertIn("17:00", heures)

    def test_jours_constant(self):
        """Test de la constante JOURS"""
        expected_days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        self.assertEqual(JOURS, expected_days)
        self.assertEqual(len(JOURS), 5)

    def test_heures_constant(self):
        """Test de la constante HEURES"""
        self.assertEqual(len(HEURES), 10)  # 9h à 18h = 10 heures
        self.assertIn("09:00", HEURES)
        self.assertIn("18:00", HEURES)
        self.assertNotIn("08:00", HEURES)
        self.assertNotIn("19:00", HEURES)

    def test_heure_range_format(self):
        """Test du format des heures retournées"""
        heures = heure_range("09:00", "11:00")
        for heure in heures:
            self.assertRegex(heure, r"\d{2}:\d{2}")
            self.assertEqual(len(heure), 5)  # Format HH:MM
