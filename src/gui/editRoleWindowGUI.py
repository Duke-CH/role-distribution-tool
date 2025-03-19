import tkinter as tk
from tkinter import ttk, messagebox

from src.data.database import Database


class EditWindow:
    def __init__(self, root, db:Database):
        self.root = root
        self.db = db
        self.conn = db.connection
        self.table_name = "Roles"
        self.original_data = []
        self.columns = []

        self.root.title("Edit Roles")
        self.root.geometry("1000x700")

        # Treeview setup
        self.tree = ttk.Treeview(self.root, show="headings")
        self.tree.pack(padx=20, pady=20, fill="both", expand=True)

        # Scrollbars
        self.scrollbar_y = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_y.pack(side="right", fill="y")

        self.scrollbar_x = ttk.Scrollbar(self.root, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side="bottom", fill="x")

        # Load database data into Treeview
        self.display_db_data()

        # Input fields and buttons
        self.inputs_frame = tk.Frame(self.root)
        self.inputs_frame.pack(pady=10)

        self.input_labels = []
        self.input_fields = []
        self.generate_input_fields()

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(pady=10)

        # Buttons
        self.save_btn = tk.Button(self.buttons_frame, text="Speichern", height=2, width=15, command=self.save_changes)
        self.save_btn.pack(side="left", padx=20)

        self.undo_btn = tk.Button(self.buttons_frame, text="Undo", height=2, width=15, command=self.undo_changes)
        self.undo_btn.pack(side="left", padx=20)

        self.cancel_btn = tk.Button(self.buttons_frame, text="Abbrechen", height=2, width=15,
                                    command=self.cancel_changes)
        self.cancel_btn.pack(side="left", padx=20)

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.populate_inputs)

        # Undo stack
        self.undo_stack = []

    def display_db_data(self):
        """
            Fetches data from the database and displays it in the Treeview widget.
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
            messagebox.showerror("Database Error", f"Error loading database: {e}")

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

    def generate_input_fields(self):
        editable_columns_db = [
            "Vorname_Position", "Nachname", "Rollengruppe", "Gender", "Essential_Next_Rest_Last",
            "just_8b", "Soziale_Beziehungen", "Thema"
        ]

        gender_options = ["Männlich", "Weiblich", "Unisex", "Divers"]
        essential_options = ["Essential", "Next", "Rest", "Last"]
        rollengruppe_options = ['Klasse 8a', 'Klasse 8b', 'Lehrkraft/Schulpersonal']
        just_8b_options = ['yes', 'no', 'next', ' ']

        try:
            cursor = self.conn.cursor()

            cursor.execute(f"PRAGMA table_info({self.table_name})")
            columns = [info[1] for info in cursor.fetchall()]

            for col in columns:
                display_name = col
                if col == "Vorname_Position":
                    display_name = "Vorname/Position"
                elif col == "Essential_Next_Rest_Last":
                    display_name = "Essential"

                label = tk.Label(self.inputs_frame, text=display_name)
                label.grid(row=len(self.input_labels), column=0, padx=10, pady=5, sticky="e")
                self.input_labels.append(label)

                if col in editable_columns_db:
                    if col == "Gender":
                        field= ttk.Combobox(self.inputs_frame, values=gender_options, state="readonly")
                    elif col == "Essential_Next_Rest_Last":
                        field = ttk.Combobox(self.inputs_frame, values=essential_options, state="readonly")
                    elif col == "Rollengruppe":
                        field = ttk.Combobox(self.inputs_frame, values=rollengruppe_options, state="readonly")
                    elif col == "just_8b":
                        field = ttk.Combobox(self.inputs_frame, values=just_8b_options, state="readonly")
                    else:
                        field = tk.Entry(self.inputs_frame)
                else:
                    field = tk.Entry(self.inputs_frame, state="disabled")

                field.grid(row=len(self.input_fields), column=1, padx=10, pady=5, sticky="w")
                self.input_fields.append(field)

        except Exception as e:
            print(f"Error generating input fields: {e}")

    def populate_inputs(self, event):
        """
        Populates the values from display table and inserts them into the tree.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            return

        EDITABLE_COLUMNS_GUI = [
            "Vorname/Position", "Nachname", "Rollengruppe", "Gender", "Essential",
            "just_8b", "Soziale_Beziehungen", "Thema"
        ]

        row_values = self.tree.item(selected_item[0])['values']
        for i, entry in enumerate(self.input_fields):
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, row_values[i])

            if self.input_labels[i]["text"] not in EDITABLE_COLUMNS_GUI:
                entry.config(state="disabled")

    def save_changes(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Fehler", "Keine Zeile ausgewählt")
            return

        old_values = self.tree.item(selected_item[0])['values']
        id_index = self.tree["columns"].index("ID")  # Replace "id" with the actual ID column name
        row_id = old_values[id_index]
        updated_values = [entry.get() for entry in self.input_fields]

        rollengruppe_index = self.tree["columns"].index("Rollengruppe")
        soziale_beziehungen_index = self.tree["columns"].index("Soziale_Beziehungen")

        rollengruppe = updated_values[rollengruppe_index]
        soziale_beziehungen = updated_values[soziale_beziehungen_index]

        # Validation
        if rollengruppe == 'Lehrkraft/Schulpersonal':
            if int(soziale_beziehungen) != 1000:  # Ensure that it's an integer comparison
                messagebox.showerror("Fehler",
                                     "Für die Lehrkraft/Schulpersonal, müssen die sozialen Beziehungen 1000 sein.")
                return
        else:
            if int(soziale_beziehungen) == 1000:
                messagebox.showerror("Fehler", "Für die Studenten, dürfen die sozialen Beziehungen nicht 1000 sein.")
                return


        cursor = self.conn.cursor()

        column_names = self.tree["columns"]
        set_clause = ", ".join([f"{col} = ?" for col in column_names[1:]])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {column_names[0]} = ?"

        try:
            cursor.execute(query, updated_values[1:] + [row_id])
            self.conn.commit()

            self.tree.item(selected_item[0], values=updated_values)

            # Save the old state for undo functionality
            self.undo_stack.append((selected_item[0], old_values))

            messagebox.showinfo("Erfolgreich", "Änderungen erfolgreich gespeichert!")

            # Ensure EditWindow retains focus after showing a dialog
            self.root.lift()
        except Exception as e:
            messagebox.showerror("Fehler", f"konnte nicht speichern: {e}")

    def undo_changes(self):
        if not self.undo_stack:
            messagebox.showerror("Fehler", "Noch keine Änderungen gemacht!")
            return

        item, old_values = self.undo_stack.pop()

        cursor = self.conn.cursor()

        column_names = self.tree["columns"]
        set_clause = ", ".join([f"{col} = ?" for col in column_names[1:]])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {column_names[0]} = ?"

        try:
            cursor.execute(query, old_values[1:] + [old_values[0]])
            self.conn.commit()

            self.tree.item(item, values=old_values)

            for i, entry in enumerate(self.input_fields):
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, old_values[i])

                if self.input_labels[i]["text"] not in [
                    "Vorname/Position", "Nachname", "Rollengruppe", "Gender", "Essential",
                    "just_8b", "Soziale_Beziehungen", "Thema"
                ]:
                    entry.config(state="disabled")

            messagebox.showinfo("Erfolgreich", "Änderungen erfolgreich rückgängig gemacht!")

            # Ensure EditWindow retains focus after showing a dialog
            self.root.lift()
        except Exception as e:
            messagebox.showerror("Fehler", f"konnte nicht rückgängig gemacht werden: {e}")

    def cancel_changes(self):
        self.root.destroy()
