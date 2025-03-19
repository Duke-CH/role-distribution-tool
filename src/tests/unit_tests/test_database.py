# Run test: PYTHONPATH=src python -m unittest src.tests.unit_tests.test_database

import unittest
import os
from sqlite3 import OperationalError
from src.data.database import Database
from src.models.role import Role

class TestDatabase(unittest.TestCase):
    """
    Unit tests for the Database class.
    Ensures database initialization, role insertion, and role fetching functionality work as expected.
    """

    def setUp(self):
        """
        Set up a temporary test database.

        Creates a new database file for testing purposes.

        Attributes:
            db_path (str): Path to the test database file.
            db (Database): Database instance connected to the test database.
        """
        self.db_path = "test_role_assignment.db"
        self.db = Database(self.db_path)

    def tearDown(self):
        """
        Clean up the test database after each test.

        Closes the database connection and removes the test database file.
        """
        self.db.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_create_tables(self):
        """
        Test that the Roles table is created successfully.

        Verifies:
        - The `Roles` table exists in the database after initialization.
        """
        self.db._initialize_database()
        result = self.db.connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Roles';")
        self.assertIsNotNone(result.fetchone())

    def test_insert_and_fetch_roles(self):
        """
        Test inserting and fetching roles from the database.

        Inserts a role into the database and verifies that it can be fetched correctly.

        Verifies:
        - The inserted role exists in the fetched roles.
        - The attributes of the fetched role match the inserted data.
        """
        # Insert a new role
        self.db.connection.execute("""
            INSERT INTO Roles (Vorname_Position, Nachname, Rollengruppe, Gender, Essential_Next_Rest_Last, just_8b, Thema, Soziale_Beziehungen)
            VALUES ('Lehrer', 'Müller', 'Klasse 8a', 'männlich', 'E', NULL, 'Inklusion', 3);
        """)
        self.db.connection.commit()

        # Fetch roles
        roles = self.db.fetch_all_roles()

        # Search for the inserted role
        inserted_role = next((role for role in roles if role.vorname_position == "Lehrer" and role.nachname == "Müller"), None)
        self.assertIsNotNone(inserted_role)
        self.assertEqual(inserted_role.gender, "männlich")

    def test_fetch_roles_with_no_data(self):
        """
        Test fetching roles when the database is empty.

        Ensures:
        - Fetching roles from an empty database returns an empty list.
        """
        # Ensure the database is empty before fetching roles
        self.db.connection.execute("DELETE FROM Roles;")
        self.db.connection.commit()
        roles = self.db.fetch_all_roles()
        self.assertEqual(roles, [])

    def test_table_exists(self):
        """
        Test the _table_exists method.

        Verifies:
        - `True` is returned for existing tables.
        - `False` is returned for non-existent tables.
        """
        self.db._initialize_database()
        self.assertTrue(self.db._table_exists("Roles"))
        self.assertFalse(self.db._table_exists("NonExistentTable"))

    def test_error_handling_for_missing_table(self):
        """
        Test that an error is raised when fetching from a missing table.

        Ensures:
        - An `OperationalError` is raised if a non-existent table is queried.
        """
        with self.assertRaises(OperationalError):
            self.db.connection.execute("SELECT * FROM NonExistentTable;")

if __name__ == "__main__":
    unittest.main()