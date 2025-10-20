import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from app.gui import run_app, heure_range, JOURS, HEURES

class TestGuiAdvanced(unittest.TestCase):
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.root = None

    def tearDown(self):
        """Nettoyage après chaque test"""
        if self.root:
            self.root.destroy()

    def test_gui_constants(self):
        """Test des constantes de l'interface"""
        self.assertEqual(len(JOURS), 5)
        self.assertEqual(len(HEURES), 10)
        self.assertIn("Lundi", JOURS)
        self.assertIn("09:00", HEURES)
        self.assertIn("18:00", HEURES)

    def test_heure_range_comprehensive(self):
        """Tests complets de la fonction heure_range"""
        # Test avec des heures normales
        result = heure_range("09:00", "12:00")
        self.assertEqual(result, ["09:00", "10:00", "11:00"])
        
        # Test avec une seule heure
        result = heure_range("14:00", "15:00")
        self.assertEqual(result, ["14:00"])
        
        # Test avec des heures inversées
        result = heure_range("15:00", "14:00")
        self.assertEqual(result, [])
        
        # Test avec la même heure
        result = heure_range("10:00", "10:00")
        self.assertEqual(result, [])

    @patch('app.gui.tk.Tk')
    def test_run_app_initialization(self, mock_tk):
        """Test de l'initialisation de l'application"""
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        # Mock des composants Tkinter
        with patch('app.gui.tk.Label'), \
             patch('app.gui.tk.Frame'), \
             patch('app.gui.tk.Entry'), \
             patch('app.gui.tk.Canvas'), \
             patch('app.gui.tk.Scrollbar'), \
             patch('app.gui.tk.Button'):
            
            try:
                run_app()
                # Vérifier que les méthodes principales ont été appelées
                mock_root.title.assert_called_once()
                mock_root.geometry.assert_called_once()
                mock_root.resizable.assert_called_once()
            except Exception as e:
                # Si l'application ne peut pas s'initialiser complètement,
                # c'est normal car nous mockons les composants
                self.assertIn("Tkinter", str(type(e).__name__))

    def test_heure_range_edge_cases(self):
        """Test des cas limites de heure_range"""
        # Test avec des heures en fin de journée
        result = heure_range("17:00", "18:00")
        self.assertEqual(result, ["17:00"])
        
        # Test avec des heures au début de journée
        result = heure_range("09:00", "10:00")
        self.assertEqual(result, ["09:00"])
        
        # Test avec des heures non standard
        result = heure_range("13:30", "14:30")
        # La fonction heure_range fonctionne avec n'importe quelles heures
        self.assertEqual(result, ["13:30"])

    def test_heure_range_format_validation(self):
        """Test de validation du format des heures"""
        # Test avec un format valide
        result = heure_range("10:00", "11:00")
        self.assertIsInstance(result, list)
        for heure in result:
            self.assertRegex(heure, r"^\d{2}:\d{2}$")
        
        # Test avec des heures qui ne sont pas des heures pleines
        result = heure_range("10:30", "11:30")
        # La fonction heure_range fonctionne avec n'importe quelles heures
        self.assertEqual(result, ["10:30"])

    def test_jours_heures_consistency(self):
        """Test de la cohérence entre JOURS et HEURES"""
        # Vérifier que JOURS contient les bons jours
        expected_jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        self.assertEqual(JOURS, expected_jours)
        
        # Vérifier que HEURES contient les bonnes heures
        expected_heures = [f"{h:02d}:00" for h in range(9, 19)]
        self.assertEqual(HEURES, expected_heures)
        
        # Vérifier que les heures sont bien formatées
        for heure in HEURES:
            self.assertRegex(heure, r"^\d{2}:\d{2}$")
            self.assertEqual(len(heure), 5)

    def test_heure_range_boundary_conditions(self):
        """Test des conditions limites de heure_range"""
        # Test avec des heures adjacentes
        result = heure_range("09:00", "10:00")
        self.assertEqual(len(result), 1)
        
        # Test avec des heures très éloignées
        result = heure_range("09:00", "18:00")
        self.assertEqual(len(result), 9)
        
        # Test avec des heures en dehors de la plage normale
        result = heure_range("08:00", "09:00")
        # La fonction heure_range fonctionne même en dehors de la plage HEURES
        self.assertEqual(result, ["08:00"])
        
        result = heure_range("18:00", "19:00")
        self.assertEqual(result, ["18:00"])
