from typing import Optional

# Represents a student participating in the role assignment process
# Each student has a first name, last name, preferred gender, and excluded gender preferences
class Student:
    
    def __init__(self, 
                 first_name: str,                 
                 last_name: str,                 
                 preferred_gender: str, # (männlich, weiblich, divers)
                 excluded_gender: Optional[str] = None): # The gender the student wants to exclude for their role

        self.first_name = first_name
        self.last_name = last_name
        self.preferred_gender = preferred_gender
        self.excluded_gender = excluded_gender  

    def __repr__(self) -> str:
        return f"<Student {self.first_name} {self.last_name}>"

    def full_name(self) -> str:
        """Returns the student's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def is_excluded_from(self, gender: str) -> bool:
        """Check if a gender is excluded by the student."""
        return self.excluded_gender is not None and self.excluded_gender == gender
