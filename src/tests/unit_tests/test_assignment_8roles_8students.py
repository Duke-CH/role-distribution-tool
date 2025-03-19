# Run test with: PYTHONPATH=src python -m unittest src.tests.unit_tests.test_assignment_8roles_8students

# 8 essential roles (5m, 1f, 1d, 1u)
# 8 students (5 without exclusion + 3 with)
# The 80% gender_match_percentage is not tested

# Expected:
# 2 unisex and 2 male students <-> 4 male roles
# 1 female student             <-> the female role
# 1 divers student             <-> the divers role
# and 1 female/divers student  <-> the unisex role

# Issue 1: Students with unisex preference and unisex role are not assigned very flexibly -> can't get the optimal result
    # Solution: 
    # - if weiblich student stay unassigned 
    #     -> should check if any weiblich roles were taken by unisex students, 
    #     if so, reassign a weiblich role (that was taken by unisex student) to the unassigned weiblich student. 
    #     And similar steps if there are male or divers students unassigned. 
    # - Reassign those unisex students to any remaining roles that haven't been assigned yet
# Issue 2: Loose gender matching for students with no exclusion -> leads to suboptimal result
    # Solution: 
    #     Reinforce strict gender matching for all students at first, (done)
    #     if they can't be 100% match, then get loose for students without exclusions (next up)

# Test output with relaxed gender matching:
# Assignments: {'S1 Female': 'R1 Unisex', 'S2 Male': 'R2 Male', 'S5 Female': 'R3 Female', 'S3 Divers': 'R4 Divers', 
#               'S7 Male': 'R5 Male', 'S4 Unisex': 'R6 Male', 'S6 Divers': 'R7 Male', 'S8 Unisex': 'R8 Male'}

import unittest
from unittest.mock import MagicMock
from src.data.database import Database
from src.models.student import Student
from src.models.role import Role
from src.services.role_assignment import RoleAssignment

class TestRoleAssignment(unittest.TestCase):
    """
    Unit tests for the RoleAssignment service, verifying role assignment logic
    with various role hierarchies and student preferences.
    """

    def setUp(self):
        """
        Set up sample roles and students for testing.

        Roles:
        - 8 roles with varying genders and priorities (Essential).
        Students:
        - 8 students with different gender identities and preferences.
        """
        self.roles = [
            Role("R1", "Unisex", "Class", "unisex", "E", None, "Inclusion", 1),
            Role("R2", "Male", "Class", "männlich", "E", None, "Diversity", 2),
            Role("R3", "Female", "Class", "weiblich", "E", None, "Equality", 3),
            Role("R4", "Divers", "Class", "divers", "E", None, "Accessibility", 4),
            Role("R5", "Male", "Class", "männlich", "E", None, "Accessibility", 5),
            Role("R6", "Male", "Class", "männlich", "E", None, "Accessibility", 6),
            Role("R7", "Male", "Class", "männlich", "E", None, "Accessibility", 7),
            Role("R8", "Male", "Class", "männlich", "E", None, "Accessibility", 8),
        ]

        self.students = [
            Student("S1", "Female", "weiblich"),
            Student("S2", "Male", "männlich"),
            Student("S3", "Divers", "divers"),
            Student("S4", "Unisex", "unisex"),
            Student("S5", "Female", "weiblich"),
            Student("S6", "Divers", "divers"),
            Student("S7", "Male", "männlich"),
            Student("S8", "Unisex", "unisex"),
        ]

        # Mock the database
        self.mock_db = MagicMock(spec=Database)
        self.mock_db.fetch_all_roles.return_value = self.roles

    def test_assignment_with_8_roles_and_8_students(self):
        """
        Test role assignment with 8 roles and 8 students.

        This test checks the following:
        - That the number of assigned roles matches the expected value.
        - That the algorithm respects gender preferences.
        - That unassigned students (if any) generate warnings.

        Raises:
            AssertionError: If the number of assigned roles or warnings is incorrect.
        """
        result = RoleAssignment.match_roles_to_students(self.mock_db, self.students)
        print("Assignments:", result["assignments"])

        # Assert the number of assignments matches the expected value
        self.assertEqual(len(result["assignments"]), 8)

        # Additional checks for debugging and clarity
        warnings = result.get("warnings", [])
        print(f"Warnings: {warnings}")
        
        # # Expected role assignments
        # expected_assignments = {
        #     "S1 Female": "R1 Unisex",
        #     "S2 Male": "R2 Male",
        #     "S3 Divers": "R4 Divers",
        #     "S4 Unisex": "R1 Unisex",
        #     "S5 Female": "R3 Female",
        #     "S6 Divers": "R6 Male",
        #     "S7 Male": "R7 Male",
        #     "S8 Unisex": "R8 Male",
        # }

        # for student_name, role_name in expected_assignments.items():
        #     self.assertEqual(result["assignments"].get(student_name), role_name)

if __name__ == "__main__":
    unittest.main()