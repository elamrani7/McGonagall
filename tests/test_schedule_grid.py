import unittest
from app.ScheduleGrid import ScheduleGrid
from app.models import Course

class TestScheduleGrid(unittest.TestCase):
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.jours = ["Lundi", "Mardi", "Mercredi"]
        self.heures = ["09:00", "10:00", "11:00", "12:00"]
        self.grid = ScheduleGrid(self.jours, self.heures)

    def test_schedule_grid_initialization(self):
        """Test de l'initialisation de la grille"""
        self.assertEqual(self.grid.jours, self.jours)
        self.assertEqual(self.grid.heures, self.heures)
        self.assertIsInstance(self.grid.grid, dict)

    def test_grid_structure(self):
        """Test de la structure de la grille"""
        for jour in self.jours:
            self.assertIn(jour, self.grid.grid)
            for heure in self.heures:
                self.assertIn(heure, self.grid.grid[jour])
                self.assertEqual(self.grid.grid[jour][heure], "")

    def test_add_course_single_hour(self):
        """Test d'ajout d'un cours d'une heure"""
        course = Course("Lundi", "Math", "M. Dupont", "09:00", "10:00", "T105", "I2")
        self.grid.add_course(course)
        
        self.assertEqual(self.grid.grid["Lundi"]["09:00"], "Math\nM. Dupont\nT105\nI2")
        self.assertEqual(self.grid.grid["Lundi"]["10:00"], "")

    def test_add_course_multiple_hours(self):
        """Test d'ajout d'un cours de plusieurs heures"""
        course = Course("Mardi", "Physique", "Mme Martin", "10:00", "12:00", "Lab1", "I1")
        self.grid.add_course(course)
        
        self.assertEqual(self.grid.grid["Mardi"]["10:00"], "Physique\nMme Martin\nLab1\nI1")
        self.assertEqual(self.grid.grid["Mardi"]["11:00"], "Physique\nMme Martin\nLab1\nI1")
        self.assertEqual(self.grid.grid["Mardi"]["12:00"], "")

    def test_add_course_invalid_day(self):
        """Test d'ajout d'un cours avec un jour invalide"""
        course = Course("Samedi", "Chimie", "M. Durand", "09:00", "10:00", "Lab2", "I3")
        self.grid.add_course(course)
        
        # La grille ne devrait pas être modifiée
        for jour in self.jours:
            for heure in self.heures:
                self.assertEqual(self.grid.grid[jour][heure], "")

    def test_add_course_invalid_time(self):
        """Test d'ajout d'un cours avec une heure invalide"""
        course = Course("Lundi", "Informatique", "M. Smith", "20:00", "21:00", "T200", "I4")
        self.grid.add_course(course)
        
        # La grille ne devrait pas être modifiée
        for jour in self.jours:
            for heure in self.heures:
                self.assertEqual(self.grid.grid[jour][heure], "")

    def test_add_multiple_courses_same_day(self):
        """Test d'ajout de plusieurs cours le même jour"""
        course1 = Course("Lundi", "Math", "M. Dupont", "09:00", "10:00", "T105", "I2")
        course2 = Course("Lundi", "Physique", "Mme Martin", "11:00", "12:00", "Lab1", "I1")
        
        self.grid.add_course(course1)
        self.grid.add_course(course2)
        
        self.assertEqual(self.grid.grid["Lundi"]["09:00"], "Math\nM. Dupont\nT105\nI2")
        self.assertEqual(self.grid.grid["Lundi"]["10:00"], "")
        self.assertEqual(self.grid.grid["Lundi"]["11:00"], "Physique\nMme Martin\nLab1\nI1")
        self.assertEqual(self.grid.grid["Lundi"]["12:00"], "")

    def test_add_course_edge_case_same_start_end(self):
        """Test d'ajout d'un cours avec même heure de début et fin"""
        course = Course("Mercredi", "Chimie", "M. Brown", "10:00", "10:00", "Lab3", "I5")
        self.grid.add_course(course)
        
        # Aucune case ne devrait être remplie
        for jour in self.jours:
            for heure in self.heures:
                self.assertEqual(self.grid.grid[jour][heure], "")

    def test_course_content_format(self):
        """Test du format du contenu du cours"""
        course = Course("Lundi", "Mathématiques", "M. Professeur", "09:00", "11:00", "Salle 101", "Classe A")
        self.grid.add_course(course)
        
        expected_content = "Mathématiques\nM. Professeur\nSalle 101\nClasse A"
        self.assertEqual(self.grid.grid["Lundi"]["09:00"], expected_content)
        self.assertEqual(self.grid.grid["Lundi"]["10:00"], expected_content)
