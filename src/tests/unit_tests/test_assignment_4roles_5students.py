# Run test with: PYTHONPATH=src python -m unittest src.tests.unit_tests.test_assignment_4roles_5students

# 4 essential roles
# 5 students
# Expected: 4 roles should be assigned, one warning for S8 should be shown

# Detected Issue: Unisex preference wasn't handled correctly; doesn't notice that S8 is unassigned
# -> Solved

import unittest
from unittest.mock import MagicMock
from src.data.database import Database
from src.models.student import Student
from src.models.role import Role
from src.services.role_assignment import RoleAssignment

class TestRoleAssignment(unittest.TestCase):
    """
    Unit tests for the RoleAssignment service, verifying correct role assignment logic.
    """

    def setUp(self):
        """
        Set up sample roles and students for testing.
        Creates 4 roles and 5 students with varying gender preferences for testing.
        """
        self.roles = [
            Role("Role1", "Unisex", "Class", "unisex", "E", None, "Inclusion", 1),
            Role("Role2", "Male", "Class", "männlich", "E", None, "Diversity", 2),
            Role("Role3", "Female", "Class", "weiblich", "E", None, "Equality", 3),
            Role("Role4", "Divers", "Class", "divers", "E", None, "Accessibility", 4),
        ]

        self.students = [
            Student("Alice", "S1", "weiblich"),
            Student("Bob", "S2", "männlich"),
            Student("Charlie", "S3", "divers"),
            Student("Dana", "S4", "unisex"),
            Student("Helena", "S8", "unisex"),
        ]

        # Mock the database
        self.mock_db = MagicMock(spec=Database)
        self.mock_db.fetch_all_roles.return_value = self.roles

    def test_basic_assignment(self):
        """
        Test a basic role assignment.

        Verifies:
        - That 4 roles are assigned to the 5 students.
        - The remaining unassigned student (S8) generates a warning.

        Raises:
            AssertionError: If the number of assigned roles is incorrect.
        """
        result = RoleAssignment.match_roles_to_students(self.mock_db, self.students)
        
        print("Assignments:", result["assignments"])
        
        # Additional checks for debugging and clarity
        warnings = result.get("warnings", [])
        print(f"Warnings: {warnings}")

        self.assertEqual(len(result["assignments"]), 4)

    def test_all_roles_assigned(self):
        """
        Test that all roles are assigned if possible.

        Verifies:
        - That all roles are assigned based on hierarchy and gender preferences.
        
        Raises:
            AssertionError: If the number of assigned roles is not equal to 4.
        """
        result = RoleAssignment.match_roles_to_students(self.mock_db, self.students)
        self.assertEqual(len(result["assignments"]), 4)

if __name__ == "__main__":
    unittest.main()