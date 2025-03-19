import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from src.data.database import Database


class DeleteWindow:
    def __init__(self, root, db:Database):
        self.original_data = []
        self.columns = []
        self.root = root
        self.db = db
        self.conn = db.connection
        self.table_name = "Roles"
        self.deleted_rows = []

        self.root.title("Delete Roles")
        self.root.geometry("1000x600")

        # Treeview widget for displaying the table
        self.tree = ttk.Treeview(self.root, show="headings")
        self.tree.pack(padx=20, pady=20, fill="both", expand=True)

        # Scrollbars for Treeview
        self.scrollbar_y = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_y.pack(side="right", fill="y")

        self.scrollbar_x = ttk.Scrollbar(self.root, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side="bottom", fill="x")

        # Load and display the database data
        self.display_db_data()

        # Delete Button
        delete_btn = tk.Button(self.root, text="Löschen", height=3, width=10, command=self.delete_selected_rows)
        delete_btn.pack(side=tk.LEFT, padx=(0, 20))

        # Undo Button
        self.undo_btn = tk.Button(self.root, text="Undo", height=3, width=10, command=self.undo_delete)
        self.undo_btn.pack(side=tk.LEFT)
        self.undo_btn.config(state=tk.DISABLED)

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

    def delete_selected_rows(self):
        """
        Deletes selected rows from the database.
        :return:
        """
        selected_items = self.tree.selection()

        if not selected_items:
            print("Nothing selected")
            return

        try:
            cursor = self.conn.cursor()

            for item in selected_items:
                # Get row values and extract the ID
                row_values = self.tree.item(item)['values']
                row_id = row_values[0]  # Assuming ID is the first column

                if row_id is None:
                    continue  # Skip if ID is missing

                # Store deleted row for undo (including ID)
                self.deleted_rows.append(row_values)

                # Remove from Treeview
                self.tree.delete(item)

                # Delete from database using ID
                query = f"DELETE FROM {self.table_name} WHERE ID = ?"
                cursor.execute(query, (row_id,))

            self.conn.commit()

            # Enable Undo button if there are deleted rows
            if self.deleted_rows:
                self.undo_btn.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error deleting rows: {e}")

    def undo_delete(self):
        """
            Restores the last deleted row to the database without overriding the ID.
        """
        if not self.deleted_rows:
            print("Nothing to undo")
            return

        try:
            last_deleted_row = self.deleted_rows.pop()  # Get last deleted row

            cursor = self.conn.cursor()

            # Get all column names including ID
            column_names = self.tree["columns"]
            placeholders = ', '.join(['?'] * len(last_deleted_row))
            query = f"INSERT INTO {self.table_name} ({', '.join(column_names)}) VALUES ({placeholders})"

            # Check if the original ID already exists
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name} WHERE ID = ?", (last_deleted_row[0],))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", f"Cannot restore: ID {last_deleted_row[0]} already exists!")
                return

            # Insert row with original ID
            cursor.execute(query, last_deleted_row)

            # Commit changes
            self.conn.commit()

            # Reinsert restored row into Treeview
            self.tree.insert('', 'end', values=last_deleted_row)

            # Disable Undo button if no more rows to undo
            if not self.deleted_rows:
                self.undo_btn.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error restoring row: {e}")