import unittest
import sqlite3
from pickletools import string1
from src.gui.addRoleWindowGUI import create_db_connection

# this class contians test cases to verify the behavior of the "create_db_connection" function
class TestDatabaseConnection(unittest.TestCase):
    def test_valid_db_connection(self):
        """
        Test if a valid db connection can be established.
        """
        # Use an in-memory SQLite db for testing
        conn = create_db_connection(":memory:")
        # Ensure the connection is not None
        self. assertIsNotNone(conn)
        # Close the connection after testing
        conn.close()

    # To verify that providing an invalid db path raises an appropriate error
    def test_invalid_db_path(self):
        """
        Test if an invalid db path returns None.
        """
        # Provide a path to an invalid directory (non-existent or no write permission)
        invalid_path = "/non_existent_directory/invalid_path_db"

        with self.assertRaises(sqlite3.OperationalError):  # Expect an OperationalError
            create_db_connection(invalid_path)


if __name__ == '__main__':
    unittest.main()