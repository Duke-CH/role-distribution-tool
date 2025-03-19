import unittest
from src.gui.addRoleWindowGUI import RoleWindow, create_db_connection
import tkinter as tk

class TestAddRoleToDB(unittest.TestCase):
    def setUp(self):
        """
        Set up an in-memory SQLite db and initilaize RoleWindow for testing.
        """
        self.conn = create_db_connection(":memory:")
        self.table_name="roles"
        self.conn.execute("""
                    CREATE TABLE roles (
                        Vorname_Position TEXT,
                        Nachname TEXT,
                        Rollengruppe TEXT,
                        Gender TEXT,
                        Essential_Next_Rest_Last TEXT,
                        just_8b TEXT,
                        Thema TEXT,
                        Soziale_Beziehungen TEXT
                    )
                """)
        self.conn.commit()

        # Create a dummy Tkinter root window
        self.root = tk.Tk()

        self.app = RoleWindow(self.root, self.conn, self.table_name)

    def tearDown(self):
        """
        Close the database connection after each test.
        """
        self.conn.close()

    def test_add_role_to_database(self):
        """
        Test adding a role to the database.
        """
        # Call the method to add a role
        self.app.add_role_to_database(
            "John", "Doe", "Schüler", "Male", "Essential", None, None, "Group1"
        )

        # Verify that the role was added to the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM roles")
        rows = cursor.fetchall()

        # Check that one row was added and matches expected values
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ("John", "Doe", "Schüler", "Male", "Essential", None, None, "Group1"))

if __name__ == "__main__":
    unittest.main()

