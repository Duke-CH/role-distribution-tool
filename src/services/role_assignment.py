import sys
sys.path.append('src')

import csv
import random
import numpy as np
from scipy.optimize import linear_sum_assignment
from typing import List, Dict, Set

from src.models.student import Student
from src.data.database import Database

class RoleAssignment:
    """
        Handles the role assignment process using a cost-based optimization approach.
    """

    def __init__(self, db: Database, students: List[Student]):
        """
            Initializes the RoleAssignment class.

            Parameters:
                - db (Database): The database instance containing role data.
                - students (List[Student]): The list of students to be assigned roles.
        """
        self.db = db
        self.students = students
        self.roles = self.dynamic_role_loading()
        self.special_groups = self.fetch_special_groups()
        self.random_prob = 0.5
        self.max_iterations = 10

        # Cost definitions for different role hierarchies
        self.cost_for_essential = 5
        self.cost_for_next = 15
        self.cost_for_rest = 20
        self.cost_for_last = 25
        self.cost_for_matched_gender = -4
        self.cost_for_special_group = -3
        self.cost_for_unisex = -2
        self.penalty_cost_for_exclusion = 1000

        self.cost_matrix = self.construct_cost_matrix()

        self.solution = []  # Stores successful assignments
        self.high_cost_assignments = []  # Stores problematic assignments
        self.not_assigned = []
        self.min_cost = None  # Stores the total cost of the assignment
        self.coverage = None

    def dynamic_role_loading(self):
        """
            Dynamically loads available roles based on the number of participants.
            If the number of students is below the participant limit, only just_8b roles are loaded.
            Otherwise, all available roles are fetched.
        """
        just8b_roles = self.db.load_roles_for_just8b()
        participant_limit = len(just8b_roles)

        # Load a limited role set if participants are few, otherwise load all roles
        roles = just8b_roles if len(self.students) < participant_limit else self.db.fetch_all_roles()

        return roles

    def construct_cost_matrix(self):
        """
            Constructs a cost matrix for role assignment based on role hierarchy and exclusion constraints.
        """
        cost_matrix = np.zeros((len(self.students), len(self.roles)))

        for i, role in enumerate(self.roles):
            if role.hierarchy == 'Essential':
                cost_matrix[:, i] += self.cost_for_essential
            elif role.hierarchy == 'Next':
                cost_matrix[:, i] += self.cost_for_next
            elif role.hierarchy == 'Rest':
                cost_matrix[:, i] += self.cost_for_rest
            elif role.hierarchy == 'Last':
                cost_matrix[:, i] += self.cost_for_last

        for i, student in enumerate(self.students):
            for j, role in enumerate(self.roles):
                if student.is_excluded_from(role.gender):
                    cost_matrix[i, j] += self.penalty_cost_for_exclusion
                if student.preferred_gender == role.gender:
                    cost_matrix[i, j] += self.cost_for_matched_gender
                if role.gender == "Unisex":
                    cost_matrix[i, j] += self.cost_for_unisex

        return cost_matrix

    def solve(self):
        """
            Solves the role assignment problem using the Hungarian algorithm (linear sum assignment).
            Assigns roles to students while minimizing the overall cost.
        """
        for _ in range(self.max_iterations):
            row_ind, col_ind = linear_sum_assignment(self.cost_matrix)
            assigned_students = set(row_ind)  # Track assigned students

            # Store the initial assignment
            for student_idx, role_idx in zip(row_ind, col_ind):
                cost = self.cost_matrix[student_idx, role_idx]
                student = self.students[student_idx]
                role = self.roles[role_idx]

                if cost >= 1000:
                    self.high_cost_assignments.append((student, role, cost))
                else:
                    self.solution.append((student, role, cost))

            # Identify unassigned students
            self.not_assigned = list(set(self.students) - {student for student, _, _ in self.solution})
            self.min_cost = self.cost_matrix[row_ind, col_ind].sum()
            self.coverage = round((len(self.solution) + len(self.high_cost_assignments)) / len(self.students) * 100, 1)

            # Handle special groups
            if self.handle_special_groups(col_ind):
                return  # Valid assignment found

    def handle_special_groups(self, col_ind):
        """
        Ensures that special groups are either fully assigned or not assigned at all.
        Returns True if a valid assignment is found, otherwise False.

        Parameters:
            - col_ind (array-like): Assigned role indices from the Hungarian algorithm.
    """
        valid = True
        assigned_roles = set(col_ind)  # Set of assigned role indices

        for group_id, role_indices in self.special_groups.items():
            assigned_count = len(role_indices & assigned_roles)  # Count assigned roles in this group

            if 0 < assigned_count < len(role_indices):  # Partial assignment detected
                if random.random() < self.random_prob:
                    # Enforce full group assignment
                    for i in role_indices:
                        self.cost_matrix[:, i] += self.cost_for_special_group  # Encourage assignment
                else:
                    # Remove group from assignment
                    for i in role_indices:
                        self.cost_matrix[:, i] += 1000  # High penalty for assignment

                valid = False  # Trigger a re-run
        return valid


    def fetch_special_groups(self):
        """
        Fetches special groups and maps them to role indices in self.roles.

        Returns:
            Dict[int, Set[int]]: A dictionary where keys are GroupIDs and values are sets of role indices.
        """
        special_groups = {}
        group_ids = self.db.fetch_special_groups_ID()

        for group_id in group_ids:
            roles_in_group = self.db.get_roles_from_group(group_id)

            # Map roles to their indices in self.roles
            role_indices = {i for i, role in enumerate(self.roles) if role.id in {r.id for r in roles_in_group}}

            if role_indices:
                special_groups[group_id] = role_indices

        return special_groups


    def print_solution(self):
        """
            Prints the role assignment results to the console.
        """
        print("\n🔹 **Zuweisungsergebnisse:**")
        print("=" * 40)
        for student, role, cost in self.solution:
            print(f"✅ {student.first_name} {student.last_name} → {role.vorname_position} {role.nachname} (Kosten: {cost})")
        print("=" * 40)
        print(f"**Gesamtkosten der Zuweisung:** {self.min_cost}")
        print(f"**Gesamtabdeckung der Zuweisung:** {self.coverage}%\n")

        if self.high_cost_assignments:
            print("\n⚠️ **Problematische Zuweisungen:**")
            for student, role, cost in self.high_cost_assignments:
                print(f"🚨 {student.first_name} {student.last_name} → {role.vorname_position} {role.nachname} (Kosten: {cost})")
            print("=" * 40)

        if self.not_assigned:
            print("\n❌ **Nicht zugewiesene Teilnehmende:**")
            for student in self.not_assigned:
                print(f"❌ {student.first_name} {student.last_name}")
            print("=" * 40)

    def write_results_to_csv(self, file_path):
        """
        Writes the role assignment results to a CSV file.

        Parameters:
            - file_path (str): The path where the CSV file will be saved.
        """
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Teilnehmende Vorname",
                "Teilnehmende Nachname",
                "Selbstzugeschriebenes Gender",
                "Veto",
                "Zugewiesene Rolle",
                "Rollen-Gender",
                "Genderwünsche erfüllt?",
                "Status"
            ])

            for student, role, cost in self.solution:
                role_gender = role.gender if role else "Keine Rolle"
                gender_fulfilled = "Ja" if role and (
                            role.gender == "Unisex" or role.gender.lower() == student.preferred_gender.lower()) else "Nein"

                writer.writerow([
                    student.first_name,
                    student.last_name,
                    student.preferred_gender,
                    student.excluded_gender if student.excluded_gender else "Kein",
                    role.vorname_position + " " + role.nachname,
                    role_gender,
                    gender_fulfilled,
                    "Erfolgreich zugewiesen"
                ])

            # Write high-cost assignments
            for student, role, cost in self.high_cost_assignments:
                writer.writerow([
                    student.first_name,
                    student.last_name,
                    student.preferred_gender,
                    student.excluded_gender if student.excluded_gender else "Kein",
                    role.vorname_position + " " + role.nachname,
                    role.gender,
                    "Nein",  # High-cost assignments are usually problematic
                    "Veto verletzt"
                ])

            # Write students who didn't get a role
            for student in self.not_assigned:
                writer.writerow([
                    student.first_name,
                    student.last_name,
                    student.preferred_gender,
                    student.excluded_gender if student.excluded_gender else "Kein",
                    "Keine Rolle",
                    "N/A",
                    "N/A",
                    "Nicht zugewiesen"
                ])