import sqlite3
import os
import sys
from typing import List
from src.models.role import Role

# Adjust the path dynamically for PyInstaller compatibility
if getattr(sys, 'frozen', False):  # Running as a PyInstaller bundle
    BASE_DIR = sys._MEIPASS
    DB_DIR = os.path.join(BASE_DIR, "db")  # Note: in frozen mode, roles.db is bundled in "db"
    DB_PATH = os.path.join(DB_DIR, "roles.db")
    SEED_PATH = os.path.join(BASE_DIR, "data", "seed.sql")  # seed.sql is bundled in "data"
else:
    # In development mode, set BASE_DIR to the project root (one level up from src/data)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_DIR = os.path.join(BASE_DIR, "data", "db")
    DB_PATH = os.path.join(DB_DIR, "roles.db")
    SEED_PATH = os.path.join(BASE_DIR, "data", "seed.sql")

# Ensure the data directory exists (only needed in development mode)
if not getattr(sys, 'frozen', False):
    os.makedirs(DB_DIR, exist_ok=True)

sys.path.append(os.path.join(BASE_DIR, "src"))


class Database:
    """
    Handles the connection to the SQLite database and provides methods for fetching roles dynamically.
    """

    def __init__(self):
        """
        Initialize the database connection with the path set to 'db/roles.db'.
        Ensures the required directory exists and initializes the database schema if necessary.
        """
        self.db_path = DB_PATH
        self.connection = None

        self._connect()
        self._initialize_database()

    def _connect(self) -> None:
        """
        Connects to the SQLite database.

        Raises:
            sqlite3.Error: If a connection to the database cannot be established.
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error connecting to database: {e}")

    def _initialize_database(self) -> None:
        """
        Initializes the database by creating tables and seeding data if they do not exist.

        Raises:
            FileNotFoundError: If the seed.sql file is missing.
        """
        if not self._table_exists("Roles"):
            print("Database not established yet. Creating and seeding the database...")
            if not os.path.exists(SEED_PATH):
                raise FileNotFoundError(f"Seed file not found at {SEED_PATH}")
            with open(SEED_PATH, "r") as seed_file:
                self.connection.executescript(seed_file.read())

    def _table_exists(self, table_name: str) -> bool:
        """
        Checks if a table exists in the database.

        Args:
            table_name (str): Name of the table to check.

        Returns:
            bool: True if the table exists, False otherwise.
        """
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        result = self.connection.execute(query).fetchone()
        return result is not None

    def fetch_all_roles(self) -> List[Role]:
        """
        Fetches all roles from the database.

        Returns:
            List[Role]: A list of Role objects representing all roles in the database.

        Raises:
            sqlite3.Error: If the query execution fails.
        """
        query = "SELECT * FROM Roles ORDER BY Essential_Next_Rest_Last, Nachname, Vorname_Position"
        try:
            rows = self.connection.execute(query).fetchall()
            return self._map_roles(rows)
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error fetching roles: {e}")

    def load_roles_for_just8b(self) -> List[Role]:
        """
        Dynamically loads roles based on the 'just8b' case rules.

        Returns:
            List[Role]: A list of Role objects filtered according to 'just8b' criteria.

        Raises:
            sqlite3.Error: If the query execution fails.
        """
        query = """
        SELECT * FROM Roles
        WHERE Rollengruppe IN ('Klasse 8b', 'Lehrkraft/Schulpersonal')
        AND (Just_8b = 'yes' OR Just_8b IS NULL OR Just_8b = '')
        """
        try:
            rows = self.connection.execute(query).fetchall()
            return self._map_roles(rows)
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error loading 'just8b' roles: {e}")

    def _map_roles(self, rows) -> List[Role]:
        """
        Maps database rows to Role objects.

        Args:
            rows: The rows fetched from the database.

        Returns:
            List[Role]: A list of Role objects created from the database rows.
        """
        return [
            Role(
                id=row["ID"],
                vorname_position=row["Vorname_Position"],
                nachname=row["Nachname"],
                rollengruppe=row["Rollengruppe"],
                gender=row["Gender"],
                hierarchy=row["Essential_Next_Rest_Last"],
                just_8b=row["just_8b"],
                thema=row["Thema"],
                soziale_beziehungen=row["Soziale_Beziehungen"],
            )
            for row in rows
        ]

    def fetch_special_groups_ID(self) -> List[int]:
        """
            Fetches all GroupID values from the SpecialGroups table.

            Returns:
                List[int]: A list of all GroupID values in the SpecialGroups table.

            Raises:
                sqlite3.Error: If the query execution fails.
            """
        query = "SELECT GroupID FROM SpecialGroups"
        try:
            rows = self.connection.execute(query).fetchall()
            return [row[0] for row in rows]  # Extract GroupID values from the fetched rows
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error fetching GroupIDs: {e}")

    def get_roles_from_group(self, group_id: int) -> List[Role]:
        """
        Fetches all roles where 'Soziale_Beziehungen' matches the given GroupID.

        Args:
            group_id (int): The GroupID to filter roles by.

        Returns:
            List[Role]: A list of Role objects belonging to the specified group.

        Raises:
            sqlite3.Error: If the query execution fails.
        """
        query = """
        SELECT * FROM Roles
        WHERE Soziale_Beziehungen = ?
        ORDER BY Essential_Next_Rest_Last, Nachname, Vorname_Position
        """
        try:
            rows = self.connection.execute(query, (group_id,)).fetchall()
            return self._map_roles(rows)  # Reuse _map_roles to convert rows to Role objects
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error fetching roles for GroupID {group_id}: {e}")

    def get_next_unused_id(self) -> int:
        """
        Finds the next available ID in the Roles table.

        Retrieves all existing IDs, sorts them, and finds the first missing integer.
        The search starts from 1.

        Returns:
            int: The next unused ID.
        """
        try:
            cursor = self.connection.cursor()

            # Get all existing IDs from the Roles table in ascending order
            cursor.execute("SELECT ID FROM Roles ORDER BY ID ASC")
            existing_ids = [row[0] for row in cursor.fetchall()]

            # Find the first missing integer starting from 1
            next_id = 1
            for id_value in existing_ids:
                if id_value == next_id:
                    next_id += 1
                else:
                    break  # Found a gap

            return next_id

        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error fetching next available ID: {e}")

    def fetch_all_group_ids(self) -> List[int]:
        """
        Fetches all unique group IDs from the 'Soziale_Beziehungen' column in the Roles table.

        Returns:
            List[int]: A list of unique group IDs.

        Raises:
            sqlite3.Error: If the query execution fails.
        """
        query = "SELECT DISTINCT Soziale_Beziehungen FROM Roles WHERE Soziale_Beziehungen IS NOT NULL ORDER BY Soziale_Beziehungen ASC"
        try:
            rows = self.connection.execute(query).fetchall()
            return [row[0] for row in rows if row[0] is not None]  # Ensure no None values are returned
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error fetching all group IDs: {e}")


    def close(self) -> None:
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
