import unittest
from src.classes.assignment import Assignment
from src.classes.student import Student
from src.classes.role import Role

# Expected CSV:
    # Student Name,Assigned Role
    # None,Elena
    # None,Josephine
    # None,Kamil
    # Taylor Divers,Teacher

class TestAssignment(unittest.TestCase):

    def setUp(self):
        # Create students
        # Sample students for no assigning
        self.students = [
            Student("Alex", "Mann", "männlich"),
            Student("Emma", "Frau", "weiblich"),
            Student("Taylor", "Divers", "divers"),
            Student("Chris", "Smith", "männlich"),
        ]

        # Create roles according to:
            # INSERT INTO Roles VALUES('Elena','Hanke','Klasse 8b','weiblich','R','','Antirassismus (Mehrsprachigkeit)',7);
            # INSERT INTO Roles VALUES('Kamil','Pirog','Klasse 8b','männlich','R','','Macho, Antirassismus',7);
            # INSERT INTO Roles VALUES('Josephine','Schubert','Klasse 8b','weiblich','R','','',7);
        self.roles = [
            Role("Elena", "Hanke", "Klasse 8b", "weiblich", "R", None, "Thema A", 7),
            Role("Josephine", "Schubert", "Klasse 8b", "weiblich", "R", None, "Thema B", 7),
            Role("Kamil", "Pirog", "Klasse 8b", "männlich", "R", None, "Thema C", 7),
            Role("Teacher", "Klein", "Lehrkraft", "unisex", "R", None, "Inklusion", 1),
        ]

        # Initialize the assignment class
        self.assignment = Assignment(self.students, self.roles)

    def test_friendship_group_not_assigned_if_incomplete(self):
        # Manually modify the matching result to simulate an incomplete group assignment
        matchR = [-1, -1, 0, -1]  # Only Elena is assigned
        self.assignment._check_friendship_group(matchR)
        self.assertEqual(matchR[0], -1)  # Elena should be unassigned

    # def test_friendship_group_assigned_together(self):
    #     # Simulate a correct group assignment
    #     matchR = [0, 1, 2, -1]  # All three roles in group 7 are assigned
    #     self.assignment._check_friendship_group(matchR)
    #     self.assertEqual(matchR[:3], [0, 1, 2])  # Elena, Josephine, and Kamil should remain assigned

    def test_role_assignment_compatibility(self):
        # Test if the roles are correctly assigned based on compatibility
        result = self.assignment.max_bpm()
        self.assertEqual(result, 3)  # There should be three successful assignments

    def test_export_to_csv(self):
        # Test the CSV export functionality
        self.assignment.max_bpm()
        with open("output/assignments.csv", "r", encoding="utf-8") as file:
            lines = file.readlines()
        self.assertTrue(len(lines) > 1)  # Check that the CSV file is not empty

if __name__ == "__main__":
    unittest.main()
