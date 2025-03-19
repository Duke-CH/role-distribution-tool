from typing import Optional

class Role:
    """
    Represents a role with attributes from the database.
    Using the attribute names in German for clarity.
    """

    def __init__(self,
                 id: int,
                 vorname_position: str,            
                 nachname: str,                    
                 rollengruppe: str,                
                 gender: str,                      
                 hierarchy: str,                   
                 just_8b: Optional[str],           
                 thema: Optional[str],             
                 soziale_beziehungen: int):       
        """
        Initializes a Role object.

        Args:
            vorname_position (str): First name of a student role, or position of a teacher/other role.
            nachname (str): Last name of the role.
            rollengruppe (str): Role group (e.g., Klasse 8a, 8b, Lehrkraft).
            gender (str): Gender of the role (e.g., unisex, männlich, weiblich, divers).
            hierarchy (str): Priority of the role (E, N, R, L).
            just_8b (Optional[str]): Indicator if the role is specific to "just8b" case.
            thema (Optional[str]): Themes associated with the role.
            soziale_beziehungen (int): Number of social relationship/friendship group.

        Attributes:
            vorname_position (str): First name or position of the role.
            nachname (str): Last name of the role.
            rollengruppe (str): Role group of the role.
            gender (str): Gender of the role.
            hierarchy (str): Priority of the role in textual form.
            just_8b (Optional[str]): Indicator for "just8b" case.
            thema (Optional[str]): Associated themes of the role.
            soziale_beziehungen (int): Social relationship group number.
        """
        self.id = id
        self.vorname_position = vorname_position
        self.nachname = nachname
        self.rollengruppe = rollengruppe
        self.gender = self._map_gender(gender)
        self.hierarchy = self._map_hierarchy(hierarchy)
        self.just_8b = just_8b
        self.thema = thema
        self.soziale_beziehungen = soziale_beziehungen

    def _map_hierarchy(self, hierarchy: str) -> str:
        """
        Ensures the hierarchy value is valid, otherwise defaults to 'Unknown'.

        Args:
            hierarchy (str): The hierarchy value from the database.

        Returns:
            str: The validated hierarchy value or 'Unknown' if invalid.
        """
        valid_hierarchies = {"Essential", "Next", "Rest", "Last"}
        return hierarchy if hierarchy in valid_hierarchies else "Unknown"

    def _map_gender(self, gender: str) -> str:
        """
        Ensures the gender value is valid, otherwise defaults to 'Unknown'.

        Args:
            gender (str): The gender value from the database.

        Returns:
            str: The validated gender value or 'Unknown' if invalid.
        """
        valid_genders = {"Männlich", "Weiblich", "Divers", "Unisex"}
        return gender if gender in valid_genders else "Unknown"

    def __repr__(self) -> str:
        """
        Returns a string representation of the Role object.

        Returns:
            str: String representation of the role.
        """
        return f"<Role {self.vorname_position} {self.nachname}>"