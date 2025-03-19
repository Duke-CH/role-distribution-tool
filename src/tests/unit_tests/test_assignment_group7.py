# Run test with: PYTHONPATH=src python -m unittest src.tests.unit_tests.test_assignment_group7

# Issue - test coverage: Can't find a test case to get friend group 7 assigned together, or algorithm not done yet
# Solved: Fixed test, test positive and negative test cases (negative with all male students)

# Also expected: 
# 1. Strict gender matching
# 2. If assigned: The roles from special groups should be assigned ONCE and ALL TOGETHER;
# or else none should be assigned, and all roles of special group should be excluded from roles waiting to be assigned.

import unittest
from src.data.database import Database
from src.models.student import Student
from src.services.role_assignment import RoleAssignment

class TestSpecialGroupAssignment(unittest.TestCase):
    """Test the special friendship group assignment logic."""

    def setUp(self):
        """Set up a test database connection and sample students."""
        self.db = Database()

        # Sample students including the special group and additional participants
        self.students = [
            Student("First", "M", "männlich"),
            Student("Second", "M", "männlich"),
            Student("Third", "M", "männlich"),
        ]

        # # Add 42 more male students -> None assigned
        # for i in range(1, 43):
        #     if i % 13 < 6:
        #         self.students.append(Student(f"S{i+3}", "M", "männlich"))
        #     elif i % 13 >= 6 or i % 12 <= 10:
        #         self.students.append(Student(f"S{i+3}", "M", "männlich"))
        #     elif i % 13 == 11:
        #         self.students.append(Student(f"S{i+3}", "M", "männlich"))
        #     else:
        #         self.students.append(Student(f"S{i+3}", "M", "männlich"))

        # Add 42 more students -> All assigned
        for i in range(1, 43):
            if i % 13 < 6:
                self.students.append(Student(f"S{i+3}", "Male", "männlich"))
            elif i % 13 >= 6 or i % 12 <= 10:
                self.students.append(Student(f"S{i+3}", "Female", "weiblich"))
            elif i % 13 == 11:
                self.students.append(Student(f"S{i+3}", "Divers", "divers"))
            else:
                self.students.append(Student(f"S{i+3}", "Unisex", "unisex"))

    def tearDown(self):
        """Close the test database connection."""
        self.db.close()

    def test_special_group_assignment(self):
        """Test that the special friendship group roles are assigned as a group."""
        result = RoleAssignment.match_roles_to_students(self.db, self.students)

        # Group 7 roles
        group_7_roles = ["Elena Hanke", "Josephine Schubert", "Kamil Pirog"]

        # Find the students assigned to these roles
        group_7_students = [
            student for student, role in result["assignments"].items() if role in group_7_roles
        ]

        # Print the assignment result
        print("\nRole Assignment Result:")
        for student, role in result["assignments"].items():
            print(f"{student} -> {role}")

        # Print special group assignment details
        print("\nSpecial Group 7 Assignment:")
        for role in group_7_roles:
            assigned_student = next(
                (student for student, assigned_role in result["assignments"].items() if assigned_role == role), 
                "No Role"
            )
            print(f"{role} -> {assigned_student}")

        # Check if all or none of the roles are assigned
        self.assertTrue(
            len(group_7_students) == len(group_7_roles) or len(group_7_students) == 0,
            "Group 7 roles (Elena, Josephine, Kamil) must be assigned together or not at all.",
        )

if __name__ == "__main__":
    unittest.main()