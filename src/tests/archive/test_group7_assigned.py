import unittest
from src.classes.assignment import Assignment
from src.classes.student import Student
from src.classes.role import Role

# Run these tests: python -m unittest src.tests.test_group7_assigned
# Warning messages/logs will be printed multiple times, but it doesn't matter!
    # because these logs are being printed every time the max_bpm() method or the _check_friendship_group() method runs in the tests

# Expected CSV:
    # Student Name,Assigned Role
    # Emma Frau,Elena
    # Alex Frau,Josephine
    # Chris Smith,Kamil
    # Taylor Divers,Teacher

class TestAssignment(unittest.TestCase):

    def setUp(self):
        # Create students
        self.students = [
            Student("Alex", "Frau", "weiblich"),
            Student("Emma", "Frau", "weiblich"),
            Student("Taylor", "Divers", "divers"),
            Student("Chris", "Smith", "männlich"),
        ]

        # Create roles
        self.roles = [
            Role("Elena", "Hanke", "Klasse 8b", "weiblich", "Rest", None, "Thema A", 7),
            Role("Josephine", "Schubert", "Klasse 8b", "weiblich", "Rest", None, "Thema B", 7),
            Role("Kamil", "Pirog", "Klasse 8b", "männlich", "Rest", None, "Thema C", 7),
            Role("Teacher", "Klein", "Lehrkraft", "unisex", "Essential", None, "Inklusion", 1),
        ]

        # Initialize the assignment class
        self.assignment = Assignment(self.students, self.roles)

    # def test_friendship_group_not_assigned_if_incomplete(self):
    #     matchR = [-1, -1, 0, -1]  # Only Elena is assigned
    #     self.assignment._check_friendship_group(matchR)
    #     self.assertEqual(matchR[0], -1)  # Elena should be unassigned

    def test_friendship_group_assigned_together(self):
        matchR = [0, 1, 2, -1]  # All three roles in group 7 are assigned
        self.assignment._check_friendship_group(matchR)
        self.assertEqual(matchR[:3], [0, 1, 2])  # Elena, Josephine, and Kamil should remain assigned

    def test_role_assignment_compatibility(self):
        result = self.assignment.max_bpm()
        # Updated expectation: All four roles should be assigned successfully
        self.assertEqual(result, 4)

    def test_export_to_csv(self):
        self.assignment.max_bpm()
        with open("output/assignments.csv", "r", encoding="utf-8") as file:
            lines = file.readlines()
        self.assertTrue(len(lines) > 1)  # Check that the CSV file is not empty

if __name__ == "__main__":
    unittest.main()