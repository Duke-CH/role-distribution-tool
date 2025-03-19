# Run test with: PYTHONPATH=src python -m unittest src.tests.unit_tests.test_dynamic_role_loading

import unittest
from src.data.database import Database
from src.models.student import Student
from src.services.role_assignment import RoleAssignment

class TestDynamicRoleLoading(unittest.TestCase):
    """
    Unit tests for dynamic role loading logic based on participant count.

    Ensures:
    - Roles for 'just8b' are loaded correctly when participant count is below the limit.
    - All roles are loaded when participant count reaches or exceeds the limit.
    """

    def setUp(self):
        """
        Set up a test database connection and sample data.

        Attributes:
            db (Database): Database instance for fetching roles.
            roles (List[Role]): List of roles fetched from the database.
            students (List[Student]): Sample students for testing dynamic role loading.
        """
        self.db = Database()

        # Sample 30 roles in the database
        self.roles = self.db.fetch_all_roles()

        # Sample 30 students
        # Can change the number to get just8b case
        self.students = [
            Student(f"S{i+1}", gender.capitalize(), gender)
            for i, gender in enumerate(
                ["weiblich", "männlich", "divers", "unisex"] * 3 + ["weiblich", "männlich"]
            )
        ]

    def tearDown(self):
        """
        Clean up the test database connection after each test.

        Closes the database connection to ensure no lingering connections.
        """
        self.db.close()

    # def test_load_roles_for_just8b(self):
    #     """Test that roles for 'just8b' are loaded correctly."""
    #     roles = self.db.load_roles_for_just8b()
    #     participant_limit = len(roles)

    #     # Print loaded roles
    #     print("\nLoaded roles for 'just8b' case:")
    #     for role in roles:
    #         print(f"{role.vorname_position} {role.nachname} - Rollengruppe: {role.rollengruppe}, Just_8b: {role.just_8b}")

    #     # Assert only just8b roles are loaded
    #     self.assertTrue(all(role.rollengruppe in ["Klasse 8b", "Lehrkraft/Schulpersonal"] for role in roles))
    #     self.assertTrue(all(role.just_8b in ["yes", None, ""] for role in roles))

    def test_reload_all_roles_if_limit_exceeded(self):
        """
        Test that all roles are loaded if the participant limit is reached.

        Steps:
        - Fetch 'just8b' roles and determine the participant limit.
        - Compare the loaded roles based on whether the student count exceeds the limit.

        Asserts:
        - When the number of students is below the limit, only 'just8b' roles are loaded.
        - When the number of students equals or exceeds the limit, all roles are loaded.
        """
        just8b_roles = self.db.load_roles_for_just8b()
        participant_limit = len(just8b_roles)

        if len(self.students) < participant_limit:
            roles = just8b_roles
        else:
            roles = self.db.fetch_all_roles()

        # Print loaded roles
        for role in roles:
            print(f"{role.vorname_position} {role.nachname} - Rollengruppe: {role.rollengruppe}, Just_8b: {role.just_8b}, Gender: {role.gender}, Hierarchy: {role.hierarchy}")

        # Assert the correct roles are loaded
        if len(self.students) >= participant_limit:
            self.assertEqual(len(roles), len(self.db.fetch_all_roles()))
        else:
            self.assertEqual(len(roles), len(just8b_roles))

if __name__ == "__main__":
    unittest.main()