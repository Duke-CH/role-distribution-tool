# Run test with: PYTHONPATH=src python -m unittest src.tests.unit_tests.test_student_and_role

import unittest
from ...models.student import Student
from ...models.role import Role

class TestStudent(unittest.TestCase):
    """Tests for the Student class."""

    def setUp(self):
        """
        Set up sample Student objects for testing.
        """
        # Students without exclusions
        self.student1 = Student("Alex", "Mann", "männlich")
        self.student2 = Student("Emma", "Frau", "weiblich")
        self.student3 = Student("Taylor", "Divers", "divers")
        self.student4 = Student("Jordan", "Case", "unisex")

        # Students with exclusions
        self.student5 = Student("Chris", "Male", "männlich", excluded_gender="weiblich")
        self.student6 = Student("Lisa", "Female", "weiblich", excluded_gender="männlich")
        self.student7 = Student("Sam", "NonBinary", "divers", excluded_gender="weiblich")

    def test_full_name(self):
        """
        Test the full_name method for generating a student's full name.

        Asserts:
            - Correct combination of first name and last name.
        """
        self.assertEqual(self.student1.full_name(), "Alex Mann")
        self.assertEqual(self.student2.full_name(), "Emma Frau")
        self.assertEqual(self.student3.full_name(), "Taylor Divers")
        self.assertEqual(self.student4.full_name(), "Jordan Case")

    def test_has_excluded_gender(self):
        """
        Test the has_excluded_gender method to verify gender exclusion logic.

        Asserts:
            - Correct identification of excluded genders.
        """
        self.assertFalse(self.student1.is_excluded_from("weiblich"))
        self.assertTrue(self.student5.is_excluded_from("weiblich"))
        self.assertTrue(self.student6.is_excluded_from("männlich"))
        self.assertTrue(self.student7.is_excluded_from("weiblich"))


class TestRole(unittest.TestCase):
    """Tests for the Role class."""

    def setUp(self):
        """
        Set up sample Role objects for testing.
        """
        # Roles with different hierarchies and genders
        self.role1 = Role("Lehrer", "Schmidt", "Klasse 8a", "unisex", "E", None, "Inklusion", 3)
        self.role2 = Role("Schulleiter", "Müller", "Klasse 8b", "divers", "N", "yes", "Diversität", 5)
        self.role3 = Role("Lehrerin", "Meier", "Klasse 8a", "weiblich", "R", None, "Inklusion", 2)
        self.role4 = Role("Lehrer", "Klein", "Klasse 8a", "männlich", "L", None, "Struktur", 4)

    def test_attributes(self):
        """
        Test Role attributes to ensure correct initialization.

        Asserts:
            - Correct values for all attributes of the Role object.
        """
        self.assertEqual(self.role1.vorname_position, "Lehrer")
        self.assertEqual(self.role1.nachname, "Schmidt")
        self.assertEqual(self.role1.rollengruppe, "Klasse 8a")
        self.assertEqual(self.role1.gender, "unisex")
        self.assertEqual(self.role1.hierarchy, "Essential")
        self.assertIsNone(self.role1.just_8b)
        self.assertEqual(self.role1.thema, "Inklusion")
        self.assertEqual(self.role1.soziale_beziehungen, 3)

    def test_map_hierarchy(self):
        """
        Test the _map_hierarchy method for correct hierarchy mapping.

        Asserts:
            - Hierarchy codes map to expected hierarchy names.
        """
        self.assertEqual(self.role1.hierarchy, "Essential")
        self.assertEqual(self.role2.hierarchy, "Next")
        self.assertEqual(self.role3.hierarchy, "Rest")
        self.assertEqual(self.role4.hierarchy, "Last")

    def test_repr(self):
        """
        Test the __repr__ method for accurate string representation of Role objects.

        Asserts:
            - String representation matches the expected format.
        """
        self.assertEqual(repr(self.role1), "<Role Lehrer Schmidt>")
        self.assertEqual(repr(self.role2), "<Role Schulleiter Müller>")
        self.assertEqual(repr(self.role3), "<Role Lehrerin Meier>")
        self.assertEqual(repr(self.role4), "<Role Lehrer Klein>")

if __name__ == "__main__":
    unittest.main()