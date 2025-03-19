import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import sqlite3

from src.data.database import Database


class AddRoleWindow:
    """
        We encapsulate the GUI in a class, which allows us to store the widgets as instance variables.
        makes it easy to access them from other methods within the class.
    """
    def __init__(self, root, db:Database):
        """
        Initializes the RoleWindow GUI for adding roles
        Args:
            root: The root window of the TKinter application
            conn: The connection object to the SQLite database
            table_name: The name of the table in the database where role data is stored
        """
        # Store the root window, db connection, table name as instance variables
        self.root = root
        self.db = db
        self.conn = db.connection
        self.table_name = "Roles"
        self.groups = self.fetch_groups_from_database()
        self.rollengruppe = self.fetch_rollengruppe_from_database()
        self.essentials = self.fetch_essential_from_database()
        self.genders = self.fetch_gender_from_database()
        self.original_data = []
        self.columns = []


        # Set the title and size of the root window
        self.root.title("Rolle hinzufügen")
        self.root.geometry("1400x700")

        # Create a canvas and scrollbar for a scrollable frame
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_frame = ttk.Frame(self.canvas)

        # Configure the canvas to update its scroll region when the frame size changes
        self.scrollbar_frame.bind("<Configure>",
                                  lambda e: self.canvas.configure(scrollregion=(self.canvas.bbox("all"))))
        self.canvas.create_window((0, 0), window=self.scrollbar_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar into the root window
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Add widgets to self.scrollable_frame
        self.create_widget()
        # Ensure fields are set correctly based on the default role
        self.toggle_fields()

        # Right frame for Treeview (Database Table)
        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Treeview for displaying database table
        self.tree = ttk.Treeview(right_frame, show="headings", height=40)
        self.tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Populate the Treeview with data from the db
        self.display_db_data()

    def create_widget(self):
        """
        Creates and configures the widgets (UI elements) for the RoleWindow GUI
        This method sets up radio buttons, labels, entry fields, comboboxes, buttons to allow
        users to input and manages role-related data.
        :return:
        """
        # Role selection (Student/Teacher) using Radio Buttons
        self.role_var = tk.StringVar(value='Schüler')

        # Label for role selection
        label_role = tk.Label(self.scrollbar_frame, text="Die hinzuzufügende Rolle:")
        label_role.pack(anchor="w", padx=20, pady=(10, 5))

        # Radio button for selecting "Schüler"
        student_radio = tk.Radiobutton(self.scrollbar_frame, text="Schüler", variable=self.role_var, value="Schüler",
                                       command=self.toggle_fields)
        student_radio.pack(anchor="w", padx=40)

        # Radio button for selecting "Lehrer"
        teacher_radio = tk.Radiobutton(self.scrollbar_frame, text="Lehrer", variable=self.role_var, value="Lehrer",
                                       command=self.toggle_fields)
        teacher_radio.pack(anchor="w", padx=40)

        # Label and Entry for first name
        label_first_name = tk.Label(self.scrollbar_frame, text="Vorname:")
        label_first_name.pack(anchor='w', padx=20, pady=(10, 10))
        self.input_first_name = tk.Entry(self.scrollbar_frame)
        self.input_first_name.pack(anchor='w', padx=40, pady=(2, 2))

        # Label and Combobox for selecting teacher type
        label_teacher_type = tk.Label(self.scrollbar_frame, text="Position:")
        label_teacher_type.pack(anchor='w', padx=20, pady=(10, 5))

        # State initially disabled since "Schüler" is selected by default
        self.teacher_type_combobox = ttk.Combobox(self.scrollbar_frame,
                                                  values=["Lehrkraft", "Förderschullehrkraft", "Schulleitung",
                                                          "Schulsozialarbeit", "Sekretariat", "Sonstiges"],
                                                  state="disabled")
        self.teacher_type_combobox.pack(anchor='w', padx=40, pady=(2, 2))
        self.teacher_type_combobox.set("Position des Lehrers wählen")

        # Add new position functionality below the topic combobox
        self.add_position_label = tk.Label(self.scrollbar_frame, text="Neue Position erstellen:")
        self.add_position_label.pack(anchor='w', padx=20, pady=(10, 5))

        self.new_position_entry = tk.Entry(self.scrollbar_frame)
        self.new_position_entry.pack(anchor='w', padx=40)

        self.add_position_btn = tk.Button(self.scrollbar_frame, text="Neue Position hinzufügen",
                                          command=self.add_new_position)
        self.add_position_btn.pack(anchor='w', padx=40, pady=(5, 10))

        # Bind event to detect selection changes
        self.teacher_type_combobox.bind("<<ComboboxSelected>>", self.update_selected_position)

        # Label and Entry for last name
        label_last_name = tk.Label(self.scrollbar_frame, text="Nachname:")
        label_last_name.pack(anchor='w', padx=20, pady=(10, 10))
        self.input_last_name = tk.Entry(self.scrollbar_frame)
        self.input_last_name.pack(anchor='w', padx=40, pady=(2, 2))

        # Label and Combobox for Rollengruppe
        label_rollengruppe = tk.Label(self.scrollbar_frame, text="Rollengruppe:")
        label_rollengruppe.pack(anchor='w', padx=20, pady=(10, 5))

        self.rollengruppe_combobox = ttk.Combobox(self.scrollbar_frame, values=self.rollengruppe)
        self.rollengruppe_combobox.pack(anchor='w', padx=40, pady=(2, 2))
        self.rollengruppe_combobox.set("Rollengruppe wählen")
        self.rollengruppe_combobox.bind("<<ComboboxSelected>>", self.update_group_based_on_rollengruppe)

        # Label and Combobox for Gender
        label_gender = tk.Label(self.scrollbar_frame, text="Geschlecht:")
        label_gender.pack(anchor='w', padx=20, pady=(10, 10))
        self.gender_combobox = ttk.Combobox(self.scrollbar_frame, values=self.genders, state="readonly")
        self.gender_combobox.pack(anchor='w', padx=40, pady=(2, 2))
        self.gender_combobox.set("Geschlecht wählen")

        # Label and Radiobutton for essential
        label_essential = tk.Label(self.scrollbar_frame, text="Essential:")
        label_essential.pack(anchor='w', padx=20, pady=(2, 2))

        self.input_essential = ttk.Combobox(self.scrollbar_frame, values=self.essentials, state="readonly")
        self.input_essential.pack(anchor='w', padx=40, pady=(2, 2))

        # Label and Combobox for just_8b
        label_just8b = tk.Label(self.scrollbar_frame, text="Just8b:")
        label_just8b.pack(anchor='w', padx=20, pady=(10, 10))

        self.just8b_combobox = ttk.Combobox(self.scrollbar_frame, values=["yes", "next", "no", "Leave Blank"],
                                            state="readonly")
        self.just8b_combobox.pack(anchor='w', padx=40, pady=(2, 2))
        self.just8b_combobox.set("Leave Blank")  # Set "Leave Blank" as teh default value

        # Label and Combobox for topic
        label_topic = tk.Label(self.scrollbar_frame, text="Thema:")
        label_topic.pack(anchor='w', padx=20, pady=(10, 10))

        # Combobox for Topic with predefines options
        self.input_topic = ttk.Combobox(self.scrollbar_frame,
                                        values=["Leave Blank", "Diversität/Rassismus/Diskriminerung (Gerechtigkeit)",
                                                "Diversität/Rassismus/Diskriminierung (Migrationshintergrund)",
                                                "Diversität/Inklusion (Lernschwäche)",
                                                "Diversität/Rassismus/Diskriminerung (Streitschlichter, Barrierefreiheit)",
                                                "Diversität/Rassismus/Diskriminerung (Non-Binär)",
                                                "Diversität/Inklusion (psychisches Problem)",
                                                "Lernschwierigkeiten/Inklusion (Strukturen im Unterricht wichtig)",
                                                "Lernschwierigkeiten/Inklusion (schriftliche Leistungen schwach)",
                                                "Lernschwierigkeiten/Inklusion (Leserechtschreibschwäche, Abschaffen von Noten)",
                                                "Lernschwierigkeiten/Inklusion (Aufmerksamkeitsprobleme, Bewegungsbedürfnis)",
                                                "Diversität/Inklusion (Hochbegabung)",
                                                "Diversität/Inklusion (Herzschrittmacher)",
                                                "Diversität/Diskriminierung (Rassismus)",
                                                "Diversität/Inklusion (Farbenblindheit)",
                                                "Inklusion/Diversität (mehrfache Klassenwiederholung)",
                                                "Inklusion/Diversität (psychisch belastet)",
                                                "Inklusion/Diversität (psychisch (familiär) belastet)",
                                                "Zuhause Notenrelevanz, Schulhund", "Nachhaltigkeit", "Antirassismus",
                                                " eventuell: Diversität/Inklusion (ADHS)",
                                                "Antirassismus (Mehrsprachigkeit)"], state="readonly")
        self.input_topic.pack(anchor='w', padx=40, pady=(2, 2))
        self.input_topic.set("Leave Blank")

        # Add new topic functionality below the topic combobox
        self.add_topic_label = tk.Label(self.scrollbar_frame, text="Neues Thema erstellen:")
        self.add_topic_label.pack(anchor='w', padx=20, pady=(10, 5))

        self.new_topic_entry = tk.Entry(self.scrollbar_frame)
        self.new_topic_entry.pack(anchor='w', padx=40)

        self.add_topic_btn = tk.Button(self.scrollbar_frame, text="Neues Thema hinzufügen", command=self.add_new_topic)
        self.add_topic_btn.pack(anchor='w', padx=40, pady=(5, 10))

        # Label and Combobox for group
        label_group = tk.Label(self.scrollbar_frame, text="Gruppe:")
        label_group.pack(anchor='w', padx=20, pady=(10, 10))

        # Fetch group option from the db and populate the combobox
        self.input_group = ttk.Combobox(self.scrollbar_frame, values=self.groups)
        self.input_group.pack(anchor='w', padx=40, pady=(2, 2))

        # Add new group functionality below the group combobox
        self.add_group_label = tk.Label(self.scrollbar_frame, text="Neue Gruppe erstellen:")
        self.add_group_label.pack(anchor='w', padx=20, pady=(10, 5))

        self.new_group_entry = tk.Entry(self.scrollbar_frame)
        self.new_group_entry.pack(anchor='w', padx=40)

        self.add_group_btn = tk.Button(self.scrollbar_frame, text="Neue Gruppe hinzufügen", command=self.add_new_group)
        self.add_group_btn.pack(anchor='w', padx=40, pady=(5, 10))

        # Confirm button
        confirm_btn = tk.Button(self.scrollbar_frame, text="Bestätigen", height=3, width=20,
                                command=self.validate_entries)
        confirm_btn.pack(anchor='w', padx=20, pady=(30, 10))

    def display_db_data(self):
        """
        Fetches data from the "roles" table in the db and displays it in a Treeview widget

        This function performs the following steps:
        1. Executed a SQL query to fetch all rows from the "roles" tables
        2. Retrieves the column names of the "roles" table using the "PRAGMA table_info" command
        3. Configures the Treeview widget to match the structure of the "roles" table
        4. Inserts the fetched rows into the Treeview for display
        5. Handles any exceptions that may occur during db operations and display an error message

        """
        try:
            cursor = self.conn.cursor()

            # Fetch all roles as Role objects
            roles = self.db.fetch_all_roles()

            # Get column names dynamically
            cursor.execute(f"PRAGMA table_info({self.table_name})")
            self.columns = [info[1] for info in cursor.fetchall()]

            # Configure treeview columns
            self.tree["columns"] = self.columns
            for col in self.columns:
                self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c, False))
                self.tree.column(col, width=100)

            # Store original data for sorting
            self.original_data = [
                (role.id, role.vorname_position, role.nachname, role.rollengruppe,
                 role.gender, role.hierarchy, role.just_8b, role.thema, role.soziale_beziehungen)
                for role in roles
            ]

            # Display the data
            self.populate_treeview(self.original_data)

        except Exception as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Laden der Datenbank: {e}")

    def populate_treeview(self, data):
        """
        Populates the treeview with given data.
        """
        self.tree.delete(*self.tree.get_children())
        for row in data:
            self.tree.insert('', 'end', values=row)

    def sort_by_column(self, col, reverse):
        """
        Sorts the treeview by a specific column.
        """
        col_index = self.columns.index(col)  # Get column index
        sorted_data = sorted(self.original_data, key=lambda x: x[col_index], reverse=reverse)

        # Update treeview with sorted data
        self.populate_treeview(sorted_data)

        # Toggle sorting order on next click
        self.tree.heading(col, text=col, command=lambda: self.sort_by_column(col, not reverse))


    def fetch_groups_from_database(self):
        """
        Fetches distinct group names form the "Soziale_Beziehungen" column in the "roles" table

        This function performs the following steps:
        1. Executes a SQL query to fetch distinct values from the "Soziale_Beziehungen" column
        2. orders the result in ascending order by the "Soziale_Beziehungen" column
        3. Extracts the group names into a list
        4. returns the list of group names

        Returns:
            list: a list of the group names. If an error occurs, the error message is displayed
        """
        try:
            # Create a cursor object to interact with the db
            cursor = self.conn.cursor()

            # Execute a SQL query to fetch distinct group names from the "Soziale_Beziehungen" column and order them in
            # ascending order
            cursor.execute("SELECT DISTINCT Soziale_Beziehungen From roles ORDER BY Soziale_Beziehungen ASC ")

            # Extract the group names from the query result and store them in a list
            groups = [row[0] for row in cursor.fetchall()]

            # Return the list of group names
            return groups

        except Exception as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen von Gruppen aus der Datenbank: {e}")
            # Return an empty list in case of an error
            return []

    def fetch_rollengruppe_from_database(self):
        """
            Fetches distinct 'Rollengruppe' values from the 'roles' table in the database.

            This function performs the following steps:
            1. Executes a SQL query to fetch distinct values from the 'Rollengruppe' column.
            2. Orders the results in ascending order.
            3. Extracts the 'Rollengruppe' values into a list.
            4. Returns the list of 'Rollengruppe' values.

            Returns:
                list: A list of distinct 'Rollengruppe' values. If an error occurs, an empty list is returned.
        """
        try:
            c = self.conn.cursor()

            # Execute a SQL query to fetch distinct "Rollengruppe" values from the "role" table and order them in
            # ascending order
            c.execute("SELECT DISTINCT Rollengruppe From roles ORDER BY Rollengruppe ASC ")

            # Extract the 'Rollengruppe' values from the query result and store them in a list
            rollengruppen = [row[0] for row in c.fetchall()]

            # Return the list of "Rollengruppe" values
            return rollengruppen

        except Exception as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen von Rollengruppen aus der Datenbank: {e}")

            # Return an empty list in case of an error
            return []

    def fetch_essential_from_database(self):
        """
            Fetches distinct 'Essential_Next_Rest_Last' values from the 'roles' table in the database.

            This function performs the following steps:
            1. Executes a SQL query to fetch distinct values from the 'Essential_Next_Rest_Last' column.
            2. Orders the results in ascending order.
            3. Extracts the 'Essential_Next_Rest_Last' values into a list.
            4. Returns the list of 'Essential_Next_Rest_Last' values.

            Returns:
                list: A list of distinct 'Essential_Next_Rest_Last' values. If an error occurs, an
                empty list is returned.
        """
        try:
            c = self.conn.cursor()

            # Query to fetch distinct Essential values
            c.execute("SELECT DISTINCT Essential_Next_Rest_Last From roles ORDER BY Essential_Next_Rest_Last ASC ")
            essentials = [row[0] for row in c.fetchall()]
            return essentials

        except Exception as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen von Essential aus der Datenbank: {e}")
            return []

    def fetch_gender_from_database(self):
        """
            Fetches distinct 'Gender' values from the 'roles' table in the database.

            This function performs the following steps:
            1. Executes a SQL query to fetch distinct values from the 'Gender' column.
            2. Orders the results in ascending order.
            3. Extracts the 'Gender' values into a list.
            4. Returns the list of 'Gender' values.

            Returns:
                list: A list of distinct 'Gender' values. If an error occurs, an empty list is returned.
        """
        try:
            c = self.conn.cursor()

            c.execute("SELECT DISTINCT Gender from roles ORDER BY Gender ASC ")
            genders = [row[0] for row in c.fetchall()]
            return genders

        except Exception as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen von Gender aus der Datenbank: {e}")
            return []

    def add_new_position(self):
        """
        Adds a new position to the db and updates the combobox with the new position.

        This method retrieves the new position from the entry widget, checks if it already exists
        in the database, and inserts it if it doesn't. The combobox is then updated to include
        the new position, and the entry field is cleared.

        Raises:
        Displays an error message if:
        - The position already exists in the database.
        - The position field is empty.
        - A database error occurs during the operation.

        """
        new_position = self.new_position_entry.get().strip()
        try:
            c = self.conn.cursor()

            # Check if topic already exists
            c.execute("SELECT COUNT(*) FROM roles WHERE Vorname_Position = ?", (new_position,))
            position_exists = c.fetchone()[0]

            if position_exists:
                messagebox.showerror("Fehler", "Position {} existiert bereits".format(new_position))
            else:
                # Update the combobox with the new topic
                current_positions = list(self.teacher_type_combobox['values'])
                current_positions.append(new_position)
                self.teacher_type_combobox['values'] = current_positions

                messagebox.showinfo("Erfolg", "Position {} wurde zur Datenbank hinzugefügt".format(new_position))

            # Clear entry field after adding
            self.new_position_entry.delete(0, END)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error fetching Essential from database: {e}")

    def add_new_topic(self):
        """
        Adds a new topic to the db and updates the combobox with the new topic.
        :return:
        """

        # Retrieve the new topic from the entry widget and strip and leading/trailing whitespace
        new_topic = self.new_topic_entry.get().strip()
        try:
            c = self.conn.cursor()

            # Check if topic already exists in the db
            c.execute("SELECT COUNT(*) FROM roles WHERE Thema = ?", (new_topic,))
            topic_exists = c.fetchone()[0]

            if topic_exists:
                # If the topic already exists, show an error message
                messagebox.showerror("Fehler", "Thema {} existiert bereits".format(new_topic))
            else:
                # Update the combobox with the new topic
                current_topics = list(self.input_topic['values'])
                current_topics.append(new_topic)
                self.input_topic['values'] = current_topics

                messagebox.showinfo("Erfolg", "Thema {} wurde zur Datenbank hinzugefügt".format(new_topic))

            # Clear entry field after adding
            self.new_topic_entry.delete(0, END)

        except Exception as e:
            # Handle any exceptions tht occur during the db operations
            messagebox.showerror("Database Error", f"Error fetching Essential from database: {e}")

    def add_new_group(self):
        """
           Adds a new group to the db and updates the combobox with the new group.

           This method retrieves the new group from the entry widget, checks if it already exists
           in the db, and inserts it if it doesn't. The combobox is then updated to include
           the new group, and the entry field is cleared.

           Raises:
               Displays an error message if:
               - The group already exists in the db.
               - A db error occurs during the operation.
           """
        new_group = self.new_group_entry.get().strip()
        try:
            c = self.conn.cursor()

            # Check if group already exists
            c.execute("SELECT COUNT(*) FROM roles WHERE Soziale_Beziehungen = ?", (new_group,))
            group_exists = c.fetchone()[0]

            if group_exists:
                messagebox.showerror("Gruppe existiert bereits", "Gruppe {} existiert bereits".format(new_group))
            else:
                # Update the combobox with the new group
                current_groups = list(self.input_group['values'])
                current_groups.append(new_group)
                self.input_group['values'] = current_groups

                messagebox.showinfo("Gruppe hinzugefügt", f"Gruppe '{new_group}' wurde hinzugefügt")

            # Clear the entry field after adding
            self.new_group_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error fetching Essential from database: {e}")

    def update_group_based_on_rollengruppe(self, event):
        """
            Updates the 'Group' field based on the selected value in the 'Rollengruppe' combobox.

            If the selected 'Rollengruppe' is "Lehrkraft/Schulpersonal", the 'Group' field is
            automatically set to "1000" and disabled for editing. For all other values of
            'Rollengruppe', the 'Group' field is enabled and cleared for user input.

            Args:
                event: The event that triggered this method (e.g., a combobox selection change).
            """

        # Get the selected value in Rollengruppe
        selected_rollengruppe = self.rollengruppe_combobox.get()

        # Check if Rollengruppe is "Lehrkraft/Schulpersonal"
        if selected_rollengruppe == "Lehrkraft/Schulpersonal":
            # Set groups value to "1000" and disable the combobox
            self.input_group.set("1000")
            self.input_group.config(state=tk.DISABLED)
        else:
            # Enable groups combobox for the other Rollengruppe values
            self.input_group.set("")
            self.input_group.config(state=tk.NORMAL)

    def update_selected_position(self, event=None):
        """
            Updates the selected position in the teacher type combobox and sets it as the default value.

            This method retrieves the currently selected value from the `teacher_type_combobox` and sets it
            as the default value in the combobox. This ensures that the selected value is displayed and
            retained as the default option.

            Args:
                event (optional): An optional event parameter, typically used when this method is triggered
                                  by an event like a button click or combobox selection change. Defaults to None.
            """
        # Get the current selected value from the combobox
        selected_position = self.teacher_type_combobox.get()

        # Set this as teh default value
        if selected_position:
            self.teacher_type_combobox.set(selected_position)

    # check if all fields are filled, if that is not the case, then msg to fill out all fields
    def validate_entries(self):
        """
            Validates if all required fields are filled out before proceeding.

            This method checks if all non-disabled fields in the form are filled out. If any required field is empty,
            it displays a warning message to the user. If all fields are valid, it proceeds to add the role to the db.

            The method handles two roles: "Lehrer" (teacher) and "Schüler" (student), with different validation rules
            for each role. For teachers, certain fields are fixed, while for students, additional fields like
            "Rollengruppe" and "Soziale_Beziehungen" are validated.
            """
        # Access the entry values using the instance variables
        Vorname_Position = self.input_first_name.get().strip() if self.input_first_name['state'] != 'disabled' else None
        Nachname = self.input_last_name.get().strip() if self.input_last_name['state'] != 'disabled' else None
        Gender = self.gender_combobox.get().strip() if self.gender_combobox['state'] != 'disabled' else None
        Essential_Next_Rest_Last = self.input_essential.get() if self.input_essential['state'] != 'disabled' else None

        # Handle Rollengruppe based on role type
        if self.role_var.get() == "Lehrer":
            # Set fixed values for Lehrer
            Rollengruppe = "Lehrkraft/Schulpersonal"
            Soziale_Beziehungen = "1000"

            # Retrieve the selected position from the combobox
            Position = self.teacher_type_combobox.get().strip()
            if not Position or Position == "Position des Lehrers wählen":
                messagebox.showwarning("Incomplete Data", "Bitte wählen Sie eine Position aus.")
                return

            # Set a placeholder value for Vorname_Position (if required)
            Vorname_Position = Position

        else:
            # Retrieve Rollengruppe for Schüler
            Rollengruppe = self.rollengruppe_combobox.get().strip()
            if not Rollengruppe or Rollengruppe == "Rollengruppe wählen":
                Rollengruppe = 0

            # Retrieve Soziale_Beziehungen only if the input_group combobox is enabled
            Soziale_Beziehungen = self.input_group.get().strip() if self.input_group['state'] != 'disabled' else None

        # Handle "Leave Blank" for just_8b
        just_8b = self.just8b_combobox.get().strip()
        if just_8b == "Leave Blank":
            just_8b = ''

        # Handle "Leave Blank" for Thema
        Thema = self.input_topic.get().strip()
        if Thema == "Leave Blank":
            Thema = ''

        # check if any field is empty (non-disabled), but allow just_8b to be None
        if (self.role_var.get() == "Schüler" and (not Vorname_Position or not Nachname or not Rollengruppe or not Gender
                                                  or not Essential_Next_Rest_Last or not Soziale_Beziehungen)) or \
                (self.role_var.get() == "Lehrer" and (not Nachname or not Essential_Next_Rest_Last)):
            messagebox.showwarning("Incomplete Data", "Alle Felder müssen eingetragen werden.")
            return

        # Call add_role_to_database with fetched values
        self.add_role_to_database(Vorname_Position, Nachname, Rollengruppe, Gender, Essential_Next_Rest_Last, just_8b,
                                  Thema, Soziale_Beziehungen)

    # For each new role that is added via the window, it gets added as a new entry in the database
    def add_role_to_database(self, *values):
        """
        Adds a new role to the database using the next available unused ID.

        This method dynamically constructs an SQL `INSERT` statement, ensuring that
        `None` values are replaced with empty strings to avoid insertion issues.
        It retrieves the next available ID before inserting the new role.

        After successfully adding the entry, the method clears the input fields,
        refreshes the Treeview widget to display the updated data, and shows a success message.

        Args:
            *values: Variable-length arguments representing the values to be inserted into
                     the database table. The order of values should match the table columns.

        Raises:
            sqlite3.Error: If there is an issue with the db operation, an error message
                           is displayed in a messagebox.
        """
        try:
            c = self.conn.cursor()

            # Fetch all column names
            c.execute(f"PRAGMA table_info({self.table_name})")
            columns = [info[1] for info in c.fetchall()]

            # Get the next available ID
            next_id = self.db.get_next_unused_id()

            # Remove 'ID' column from column list for insertion
            columns_without_id = [col for col in columns if col.lower() != "id"]

            if len(values) != len(columns_without_id):
                raise ValueError(f"Expected {len(columns_without_id)} values, but got {len(values)}")

            # Construct the INSERT statement, explicitly specifying the ID
            column_names = ", ".join(["ID"] + columns_without_id)
            placeholders = ", ".join(["?"] * (len(values) + 1))  # +1 for ID
            insert_query = f"INSERT INTO {self.table_name} ({column_names}) VALUES ({placeholders})"

            # Insert new row with the manually assigned ID
            c.execute(insert_query, (next_id, *values))
            self.conn.commit()

            messagebox.showinfo("Erfolg", "Rolle wurde hinzugefügt")
            self.clear_inputs()
            self.display_db_data()  # Refresh Treeview

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", f"Error adding role to database: {error}")

    def clear_inputs(self):
        """
        Clears all input fields and resets comboboxes to their default states.

        This method is used to reset the form by clearing text entries and resetting comboboxes
        to their initial or default values. It ensures that the form is ready for new input.
        """
        # Clear text entries
        self.input_first_name.delete(0, tk.END)
        self.input_last_name.delete(0, tk.END)

        # Reset Comboboxes
        self.gender_combobox.set("")
        self.input_topic.set("Leave Blank")
        self.input_group.set("")
        self.just8b_combobox.set("Leave Blank")
        self.input_essential.set("")

    def toggle_fields(self):
        """
            Enable or disable specific fields in the GUI based on the selected role.

            This method dynamically adjusts the state (enabled/disabled) of various input fields,
            comboboxes, and buttons depending on whether the selected role is "Lehrer" (Teacher)
            or another role (e.g., "Schüler" - Student). It ensures that only relevant fields are
            editable or visible based on the user's role selection.

            Fields affected include:
            - Teacher type combobox
            - Rollengruppe (role group) combobox
            - First name input field
            - Group and topic-related fields
            - Position-related fields
            - Gender selection combobox

            The method is typically triggered when the user changes the role selection in the GUI.
            """
        # Get the selected role from the role variable
        role = self.role_var.get()

        if role == "Lehrer": # If the selected role is "Lehrer"
            # Enable teacher type combobox and retain last selected value if available
            self.teacher_type_combobox.config(state="readonly")
            if not self.teacher_type_combobox.get():
                self.teacher_type_combobox.set("Lehrkraft")

            # Set Rollengruppe to "Lehrkraft/Schulpersonal" and disable the combobox
            self.rollengruppe_combobox.set("Lehrkraft/Schulpersonal")
            self.rollengruppe_combobox.config(state=tk.DISABLED)

            # Disable fields for specific for "Schüler"
            self.input_first_name.config(state=tk.DISABLED)
            self.new_group_entry.config(state=tk.DISABLED)
            self.add_group_btn.config(state=tk.DISABLED)
            self.add_topic_btn.config(state=tk.DISABLED)

            # Enable position-related fields for "Lehrer"
            self.new_position_entry.config(state=tk.NORMAL)  # Enable entry for new position
            self.add_position_btn.config(state=tk.NORMAL)  # Enable button for new position

            # Enable teacher type combobox
            self.teacher_type_combobox.config(state="readonly")  # Allow selection of teacher type

        else:
            # Enable Rollengruppe combobox for selection
            self.rollengruppe_combobox.set("")
            self.rollengruppe_combobox.config(state="readonly")

            # Enable fields specific Schüler
            self.input_first_name.config(state=tk.NORMAL)
            self.input_topic.config(state=tk.NORMAL)
            self.input_group.config(state=tk.NORMAL)
            self.new_group_entry.config(state=tk.NORMAL)

            self.new_position_entry.config(state="disabled")  # Enable entry for new position
            self.add_position_btn.config(state="disabled")  # Enable button for new position

            # Enable gender selection
            self.gender_combobox.config(state="readonly")  # Allow user to select gender

            # Disable teacher type combobox
            self.teacher_type_combobox.set("Lehrer Typ wählen")  # Reset place holder
            self.teacher_type_combobox.config(state="disabled")  # Disable teacher type selection

            # Disable Position Entrybox und Button



