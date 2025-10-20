import unittest
from app.models import Course

class TestCourse(unittest.TestCase):
    def test_course_initialization(self):
        c = Course("Lundi", "Math", "Mme Dupont", "09:00", "11:00", "T105", "I2 EISI")
        self.assertEqual(c.day, "Lundi")
        self.assertEqual(c.subject, "Math")
        self.assertEqual(c.teacher, "Mme Dupont")
        self.assertEqual(c.start_time, "09:00")
        self.assertEqual(c.end_time, "11:00")
        self.assertEqual(c.room, "T105")
        self.assertEqual(c.classe, "I2 EISI")

    def test_course_initialization_minimal(self):
        """Test avec les paramètres minimaux"""
        c = Course("Mardi", "Physique", "M. Martin", "14:00", "16:00")
        self.assertEqual(c.day, "Mardi")
        self.assertEqual(c.subject, "Physique")
        self.assertEqual(c.teacher, "M. Martin")
        self.assertEqual(c.start_time, "14:00")
        self.assertEqual(c.end_time, "16:00")
        self.assertEqual(c.room, "")
        self.assertEqual(c.classe, "")

    def test_course_string_representation(self):
        """Test de la représentation string du cours"""
        c = Course("Mercredi", "Chimie", "Mme Durand", "10:00", "12:00", "Lab1", "I1")
        # Vérifier que tous les attributs sont accessibles
        self.assertIsInstance(c.day, str)
        self.assertIsInstance(c.subject, str)
        self.assertIsInstance(c.teacher, str)
        self.assertIsInstance(c.start_time, str)
        self.assertIsInstance(c.end_time, str)
        self.assertIsInstance(c.room, str)
        self.assertIsInstance(c.classe, str)

    def test_course_with_empty_values(self):
        """Test avec des valeurs vides"""
        c = Course("", "", "", "", "", "", "")
        self.assertEqual(c.day, "")
        self.assertEqual(c.subject, "")
        self.assertEqual(c.teacher, "")
        self.assertEqual(c.start_time, "")
        self.assertEqual(c.end_time, "")
        self.assertEqual(c.room, "")
        self.assertEqual(c.classe, "")