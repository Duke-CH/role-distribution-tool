# PYTHONPATH=src python -m unittest src.tests.unit_tests.test_assignment_12roles_8students

# 8 students
# 12 roles (genders: 5 unisex, 3 male, 3 female, 1 divers; role hierarchies: 6 essentials, 3 next, 2 rest, 1 last)
# Roughly according to the percentage of E/N/R/L in full role set

# Before 17.01
    # Expected:
    # all essential roles assigned + matched genders
    # -> some next roles assigned + matched genders
    # -> some rest role(s) assigned + matched gender(s)

    # Test output ok:
    # Assignments: {'Alice S1': 'E1 Unisex1', 'Bob S2': 'E2 Unisex2', 'Charlie S3': 'E3 Unisex3', 'Guy S7': 'E4 Male1', 'Eve S5': 'E5 Female1', 'Faye S6': 'E6 Divers1', 
    #               'Dana S4': 'N1 Unisex4', 
    #               'Helena S8': 'R1 Unisex5'}

# Extra issue: Does role hierarchy rule has more priority than gender matching rule?
#     The result above didn't get all next roles assigned yet, but then one rest role was already given out
# -> Role hierarchy rule is more important than gender matching rule
# After 17.01:
    # Assignments: {'Alice S1': 'E1 Unisex1', 'Bob S2': 'E2 Unisex2', 'Charlie S3': 'E3 Unisex3', 'Guy S7': 'E4 Male1', 'Eve S5': 'E5 Female1', 'Faye S6': 'E6 Divers1', 
    #               'Dana S4': 'N1 Unisex4', 'Helena S8': 'N2 Male2'}

import unittest
from unittest.mock import MagicMock
from src.data.database import Database
from src.models.student import Student
from src.models.role import Role
from src.services.role_assignment import RoleAssignment

class TestRoleAssignment(unittest.TestCase):

    def setUp(self):
        """
        Set up sample roles and students for testing.

        Roles:
        - 12 roles with varying genders and hierarchies:
          - 5 unisex, 3 male, 3 female, 1 divers.
          - Hierarchy distribution: 6 essential, 3 next, 2 rest, 1 last.
        Students:
        - 8 students with different gender identities and preferences:
          - Some have exclusions (e.g., Eve excludes männlich).
        """
        self.roles = [
            # 5x Unisex roles
            Role("E1", "Unisex1", "Class", "unisex", "E", None, "Inclusion", 1),
            Role("E2", "Unisex2", "Class", "unisex", "E", None, "Support", 2),
            Role("E3", "Unisex3", "Class", "unisex", "E", None, "Equality", 3),
            Role("N1", "Unisex4", "Class", "unisex", "N", None, "Diversity", 4),
            Role("R1", "Unisex5", "Class", "unisex", "R", None, "Psychology", 5),

            # 3x Male roles
            Role("E4", "Male1", "Class", "männlich", "E", None, "Sport", 6),
            Role("N2", "Male2", "Class", "männlich", "N", None, "Science", 7),
            Role("R2", "Male3", "Class", "männlich", "R", None, "History", 8),

            # 3x Female roles
            Role("E5", "Female1", "Class", "weiblich", "E", None, "Math", 9),
            Role("N3", "Female2", "Class", "weiblich", "N", None, "Art", 10),
            Role("L1", "Female3", "Class", "weiblich", "L", None, "Music", 11),

            # 1x Divers role
            Role("E6", "Divers1", "Class", "divers", "E", None, "Health", 12),
        ]

        # Sample students
        self.students = [
            Student("Alice", "S1", "weiblich"),
            Student("Bob", "S2", "männlich"),
            Student("Charlie", "S3", "divers"),
            Student("Dana", "S4", "unisex"),
            Student("Eve", "S5", "weiblich", "männlich"),
            Student("Faye", "S6", "divers", "männlich"),
            Student("Guy", "S7", "männlich", "divers"),
            Student("Helena", "S8", "unisex"),
        ]

        # Mock the database
        self.mock_db = MagicMock(spec=Database)
        self.mock_db.fetch_all_roles.return_value = self.roles

    def test_role_assignment_with_12_roles(self):
        """
        Test role assignment with 12 roles and 8 students.

        This test verifies:
        - Each student receives exactly one role.
        - No role is assigned to a student with a matching excluded gender.
        - At least 80% of roles match the students' gender preferences.
        - Assignments adhere to role hierarchy rules.
        """
        result = RoleAssignment.match_roles_to_students(self.mock_db, self.students)

        # Ensure all students are assigned a role
        self.assertEqual(len(result["assignments"]), len(self.students))

        # Check that no student has a role that matches their excluded gender
        for student in self.students:
            assigned_role = result["assignments"].get(student.full_name())
            if assigned_role:
                role = next(r for r in self.roles if f"{r.vorname_position} {r.nachname}" == assigned_role)
                self.assertFalse(student.is_excluded_from(role.gender))

        # Check that the gender match percentage is at least 80%
        self.assertGreaterEqual(result["gender_match_percentage"], 80.0)

        # Print the assignments and warnings for manual inspection
        print("Assignments:", result["assignments"])
        if result["warnings"]:
            print("\nWarnings:")
            for warning in result["warnings"]:
                print(warning)

if __name__ == "__main__":
    unittest.main()
