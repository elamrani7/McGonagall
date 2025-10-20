import unittest
import app.index
from app.models import Course

class TestIndex(unittest.TestCase):
    def test_main_exists(self):
        self.assertTrue(hasattr(app.index, "main"))

    def test_main_runs(self):
        try:
            app.index.main()
        except Exception:
            self.fail("main() raised an exception unexpectedly")

    def test_parse_schedule_empty_html(self):
        """Test du parsing avec un HTML vide"""
        html = ""
        courses = app.index.parse_schedule(html)
        self.assertEqual(courses, [])

    def test_parse_schedule_invalid_html(self):
        """Test du parsing avec un HTML invalide"""
        html = "<html><body>Pas de cours ici</body></html>"
        courses = app.index.parse_schedule(html)
        self.assertEqual(courses, [])

    def test_parse_schedule_valid_html(self):
        """Test du parsing avec un HTML valide contenant des cours"""
        html = """
        <html>
        <body>
            <div class="innerCase">
                <div class="BackGroundCase">
                    <table class="TCase">
                        <tr><td class="TCase">Mathématiques</td></tr>
                        <tr><td class="TCProf">M. Dupont<br/>I2 EISI</td></tr>
                        <tr><td class="TChdeb">09:00-11:00</td></tr>
                        <tr><td class="TCSalle">T105</td></tr>
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
        courses = app.index.parse_schedule(html)
        self.assertIsInstance(courses, list)
        if courses:
            self.assertIsInstance(courses[0], Course)

    def test_parse_schedule_multiple_courses(self):
        """Test du parsing avec plusieurs cours"""
        html = """
        <html>
        <body>
            <div class="innerCase">
                <div class="BackGroundCase">
                    <table class="TCase">
                        <tr><td class="TCase">Mathématiques</td></tr>
                        <tr><td class="TCProf">M. Dupont<br/>I2 EISI</td></tr>
                        <tr><td class="TChdeb">09:00-11:00</td></tr>
                        <tr><td class="TCSalle">T105</td></tr>
                    </table>
                </div>
            </div>
            <div class="innerCase">
                <div class="BackGroundCase">
                    <table class="TCase">
                        <tr><td class="TCase">Physique</td></tr>
                        <tr><td class="TCProf">Mme Martin<br/>I1</td></tr>
                        <tr><td class="TChdeb">14:00-16:00</td></tr>
                        <tr><td class="TCSalle">Lab1</td></tr>
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
        courses = app.index.parse_schedule(html)
        self.assertIsInstance(courses, list)
        self.assertGreaterEqual(len(courses), 1)

    def test_parse_schedule_malformed_html(self):
        """Test du parsing avec un HTML malformé"""
        html = "<html><body><div class='innerCase'><div class='BackGroundCase'><table class='TCase'><tr><td class='TCase'>Math</td></tr></table></div></div></body></html>"
        courses = app.index.parse_schedule(html)
        # Le parsing devrait gérer les erreurs gracieusement
        self.assertIsInstance(courses, list)

    def test_parse_schedule_with_exception_handling(self):
        """Test du parsing avec gestion d'exceptions"""
        # HTML qui pourrait causer des exceptions lors du parsing
        html = """
        <html>
        <body>
            <div class="innerCase">
                <div class="BackGroundCase">
                    <table class="TCase">
                        <tr><td class="TCase">Math</td></tr>
                        <tr><td class="TCProf">Prof<br/>Classe</td></tr>
                        <tr><td class="TChdeb">09:00-11:00</td></tr>
                        <tr><td class="TCSalle">Salle</td></tr>
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
        courses = app.index.parse_schedule(html)
        self.assertIsInstance(courses, list)

    def test_parse_schedule_no_inner_case(self):
        """Test du parsing sans div innerCase"""
        html = "<html><body><div>Pas de cours ici</div></body></html>"
        courses = app.index.parse_schedule(html)
        self.assertEqual(courses, [])

    def test_parse_schedule_no_background_case(self):
        """Test du parsing sans div BackGroundCase"""
        html = """
        <html>
        <body>
            <div class="innerCase">
                <div>Pas de BackGroundCase</div>
            </div>
        </body>
        </html>
        """
        courses = app.index.parse_schedule(html)
        self.assertEqual(courses, [])

    def test_parse_schedule_no_table(self):
        """Test du parsing sans table TCase"""
        html = """
        <html>
        <body>
            <div class="innerCase">
                <div class="BackGroundCase">
                    <div>Pas de table</div>
                </div>
            </div>
        </body>
        </html>
        """
        courses = app.index.parse_schedule(html)
        self.assertEqual(courses, [])

    def test_parse_schedule_partial_course_data(self):
        """Test du parsing avec des données de cours partielles"""
        html = """
        <html>
        <body>
            <div class="innerCase">
                <div class="BackGroundCase">
                    <table class="TCase">
                        <tr><td class="TCase">Math</td></tr>
                        <!-- Pas de prof, pas d'heure, pas de salle -->
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
        courses = app.index.parse_schedule(html)
        self.assertIsInstance(courses, list)
        if courses:
            course = courses[0]
            self.assertEqual(course.subject, "Math")
            self.assertEqual(course.teacher, "Inconnu")
            self.assertEqual(course.start_time, "00:00")
            self.assertEqual(course.end_time, "00:00")
            self.assertEqual(course.room, "Inconnu")
            self.assertEqual(course.classe, "Inconnu")

    def test_parse_schedule_teacher_with_multiple_lines(self):
        """Test du parsing avec un prof ayant plusieurs lignes"""
        html = """
        <html>
        <body>
            <div class="innerCase">
                <div class="BackGroundCase">
                    <table class="TCase">
                        <tr><td class="TCase">Math</td></tr>
                        <tr><td class="TCProf">M. Dupont<br/>I2 EISI<br/>Ligne supplémentaire</td></tr>
                        <tr><td class="TChdeb">09:00-11:00</td></tr>
                        <tr><td class="TCSalle">T105</td></tr>
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
        courses = app.index.parse_schedule(html)
        self.assertIsInstance(courses, list)
        if courses:
            course = courses[0]
            self.assertEqual(course.teacher, "M. Dupont — T105")
            self.assertEqual(course.classe, "I2 EISI")

    def test_parse_schedule_time_without_dash(self):
        """Test du parsing avec un temps sans tiret"""
        html = """
        <html>
        <body>
            <div class="innerCase">
                <div class="BackGroundCase">
                    <table class="TCase">
                        <tr><td class="TCase">Math</td></tr>
                        <tr><td class="TCProf">M. Dupont<br/>I2</td></tr>
                        <tr><td class="TChdeb">09:00</td></tr>
                        <tr><td class="TCSalle">T105</td></tr>
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
        courses = app.index.parse_schedule(html)
        self.assertIsInstance(courses, list)
        if courses:
            course = courses[0]
            self.assertEqual(course.start_time, "00:00")
            self.assertEqual(course.end_time, "00:00")
