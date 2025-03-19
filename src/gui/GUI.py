import sys
sys.path.append('src')

import pandas as pd
import sqlite3
import os
import tkinter as tk
import traceback
from tkinter import filedialog, scrolledtext, messagebox

from src.services.role_assignment import RoleAssignment
from src.data.database import Database
from src.models.student import Student
from src.gui.deleteRoleWindowGUI import DeleteWindow
from src.gui.editRoleWindowGUI import EditWindow
from src.gui.addRoleWindowGUI import AddRoleWindow
from src.data.database import SEED_PATH, DB_PATH

# Global list for students
students_list = []

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Rollenverteilungs-Tool")
        self.db = Database()
        self.root.geometry ("2000x1600")

        # Button to delete a role
        delete_button = tk.Button(root, text="Rolle löschen", command=self.open_delete_window)
        delete_button.pack(pady=5)

        # Button to add a role
        add_button = tk.Button (root, text= "Rolle hinzufügen", command=self.open_add_window)
        add_button.pack(pady=5)

        # Button to edit a role
        edit_button = tk.Button(root, text="Rolle ändern", command=self.open_edit_window)
        edit_button.pack(pady=5)

        # --- Special Groups Selection UI ---
        tk.Label(root, text="Spezialgruppen auswählen:").pack()
        self.group_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=6)
        self.group_listbox.pack(pady=5)
        # Load available group IDs from Roles and preselect those already in SpecialGroups
        self.load_group_ids()

        save_groups_button = tk.Button(root, text="Spezialgruppen speichern", command=self.save_special_groups)
        save_groups_button.pack(pady=5)

        # Button to load the CSV file
        load_button = tk.Button(root, text="LimeSurvey-Daten importieren", command=self.load_csv)
        load_button.pack(pady=1)

        # ScrolledText widget to display output messages
        self.output_text = scrolledtext.ScrolledText(self.root, width=60, height=15, wrap=tk.WORD)
        self.output_text.pack(pady=1)

        # Button to assign charactersa
        assign_button = tk.Button(root, text="Rollenverteilung starten", command=self.assign_roles)
        assign_button.pack(pady=10)

        # Button to restore database
        restore_db_button = tk.Button(root, text="Datenbank wiederherstellen", command=self.restore_database)
        restore_db_button.pack(pady=5)

    def open_delete_window(self):
        # Create a new Toplevel window for DeleteWindow
        delete_window = tk.Toplevel(self.root)
        DeleteWindow(delete_window, self.db)
        delete_window.wait_window()
        self.load_group_ids()

    def open_add_window(self):
        # Create a new Toplevel window for DeleteWindow
        add_window = tk.Toplevel(self.root)
        AddRoleWindow(add_window, self.db)
        add_window.wait_window()
        self.load_group_ids()

    def open_edit_window(self):
        # Create a new Toplevel window for DeleteWindow
        edit_window = tk.Toplevel(self.root)
        EditWindow(edit_window, self.db)
        edit_window.wait_window()
        self.load_group_ids()

    def load_group_ids(self):
        """
        Loads all unique group IDs from the Roles table and preselects those already
        present in the SpecialGroups table.
        """
        try:
            # Fetch all unique group IDs from the Roles table
            all_group_ids = self.db.fetch_all_group_ids()
            # Fetch group IDs that are already marked as special
            special_group_ids = self.db.fetch_special_groups_ID()

            self.group_listbox.delete(0, tk.END)
            for idx, group in enumerate(all_group_ids):
                self.group_listbox.insert(tk.END, group)
                if group in special_group_ids:
                    self.group_listbox.selection_set(idx)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Gruppen: {e}")

    def save_special_groups(self):
        """
        Saves the user's selected special group IDs to the SpecialGroups table.
        Existing entries are cleared first.
        """
        selected_indices = self.group_listbox.curselection()
        selected_groups = [self.group_listbox.get(i) for i in selected_indices]
        try:
            conn = self.db.connection
            cursor = conn.cursor()

            # Clear existing special groups
            cursor.execute("DELETE FROM SpecialGroups")

            # Insert the newly selected group IDs
            for group in selected_groups:
                cursor.execute("INSERT INTO SpecialGroups (GroupID) VALUES (?)", (group,))

            conn.commit()

            messagebox.showinfo("Erfolg", "Spezialgruppen wurden erfolgreich gespeichert.")
            # Reload the group list to reflect any changes
            self.load_group_ids()

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern der Spezialgruppen: {e}")

    def restore_database(self):
        """
        Restores the database by reading 'seed.sql' and executing its statements.
        Closes the current DB connection and reinitializes it afterward.
        """
        # Ask user for confirmation before restoring
        confirm = messagebox.askyesno("Bestätigung",
                                      "Möchten Sie die Datenbank wirklich wiederherstellen? Alle aktuellen Daten werden überschrieben.")
        if not confirm:
            return

        try:
            if not os.path.exists(SEED_PATH):
                messagebox.showerror("Fehler", f"Seed file not found at {SEED_PATH}")
                return

            # 1) Close the existing DB connection (if open)
            self.db.close()

            # Read the seed file
            with open(SEED_PATH, "r", encoding="utf-8") as f:
                seed_script = f.read()

            # 2) Create a new temporary connection to execute the script
            temp_conn = sqlite3.connect(DB_PATH)
            temp_conn.executescript(seed_script)
            temp_conn.commit()
            temp_conn.close()

            # 3) Re-initialize the main Database connection
            self.db = Database()

            messagebox.showinfo("Erfolg", "Datenbank wurde erfolgreich wiederhergestellt.")

            # 4) Optional: Reload group IDs or refresh the UI
            self.load_group_ids()

        except Exception as e:
            messagebox.showerror("Fehler", f"Datenbank-Wiederherstellung fehlgeschlagen: {e}")

    # Function to load and display the CSV file in the text area
    def load_csv(self):
        """Load and process the CSV file."""
        global students_list

        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        self.output_text.delete(1.0, tk.END)  # Clear existing text

        # Define the column mapping for LimeSurvey data
        column_mapping = {
            "Geben Sie ihren Vor- und Nachnamen an. [Nachname]": "last_name",
            "Geben Sie ihren Vor- und Nachnamen an. [Vorname]": "first_name",
            "Welches Geschlecht schreiben Sie sich selbst zu?": "gender",
            "Gibt es ein Geschlecht, das Sie auf keine Fall spielen wollen?": "excluded_gender",
        }

        try:
            # Load the CSV file
            df = pd.read_csv(file_path, index_col=False)

            # Rename columns to match internal naming
            df = df.rename(columns=column_mapping)

            # Replace NaN in 'excluded_gender' with "Kein"
            df["excluded_gender"] = df["excluded_gender"].fillna("Kein")

            # Check for missing columns
            missing_columns = [col for col in column_mapping.values() if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Fehlende Spalten in der CSV-Datei: {', '.join(missing_columns)}")

            # Populate the global students list
            students_list = [
                Student(row["first_name"], row["last_name"], row["gender"], row["excluded_gender"])
                for _, row in df.iterrows()
            ]

            # Display loaded data in the GUI
            self.output_text.insert(tk.END, "CSV-Datei erfolgreich geladen und Studierende verarbeitet.\n")
            self.output_text.insert(tk.END, "Geladene Studierende:\n")
            self.output_text.insert(tk.END, "-" * 50 + "\n")
            self.output_text.insert(tk.END, f"{'Nachname':<15}{'Vorname':<15}{'Geschlecht':<15}{'Veto':<15}\n")
            self.output_text.insert(tk.END, "-" * 50 + "\n")
            for student in students_list:
                veto = student.excluded_gender if student.excluded_gender else "Kein"
                self.output_text.insert(tk.END,
                                        f"{student.last_name:<15}{student.first_name:<15}{student.preferred_gender:<15}{veto:<15}\n")
            self.output_text.insert(tk.END, "-" * 50 + "\n")
            self.output_text.see(tk.END)

        except Exception as e:
            self.output_text.insert(tk.END, f"Fehler beim Laden der CSV-Datei: {e}\n")
            self.output_text.see(tk.END)

    # Assign roles and generate output CSV
    def assign_roles(self):
        """Starts the role distribution process."""
        if not students_list:
            self.output_text.insert(tk.END, "Keine Studierende geladen. Bitte laden Sie zuerst eine CSV-Datei.\n")
            self.output_text.see(tk.END)
            return

        self.output_text.delete(1.0, tk.END)  # Clear existing text
        self.output_text.insert(tk.END, "Rollenverteilung wird gestartet...\n")

        try:
            # Run the role assignment algorithm
            solver = RoleAssignment(self.db, students_list)
            solver.solve()

            # Display results in the GUI
            self.output_text.insert(tk.END, "Rollenverteilung ist abgeschlossen!\n")
            self.output_text.insert(tk.END, "Ergebnis:\n")

            for student, role, cost in solver.solution:
                self.output_text.insert(tk.END,
                                        f"✅ {student.first_name} {student.last_name} -> {role.vorname_position} {role.nachname}\n")

            if len(solver.students) > len(solver.roles):
                self.output_text.insert(
                    tk.END,
                    f"!!! Achtung: Es gibt mehr Studierende ({len(solver.students)}) als verfügbare Rollen ({len(solver.roles)})\n"
                )

            if solver.high_cost_assignments:
                self.output_text.insert(tk.END, "\n⚠️ **Problematische Zuweisungen:**\n")
                for student, role, cost in solver.high_cost_assignments:
                    self.output_text.insert(tk.END,
                                            f"🚨 {student.first_name} {student.last_name} -> {role.vorname_position} {role.nachname}\n")

            # Ask user where to save the result CSV
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Speichern Sie das Ergebnis der Rollenverteilung"
            )
            if file_path:
                solver.write_results_to_csv(file_path)
                self.output_text.insert(tk.END, f"Ergebnis wurde gespeichert: {file_path}\n")

        except Exception as e:
            self.output_text.insert(tk.END, f"Fehler während der Rollenverteilung: {e}\n")

            # Bugfix: print the error, this line could be omitted later
            print(traceback.format_exc())
        finally:
            self.output_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

