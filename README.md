# Role Distribution Tool
This project was developed by a team of four students from the Technical University of Darmstadt to improve the 
efficiency of a seminar course at the university.

## Features
1. The assignment algorithm ensures fairness among students and speeds up the entire assignment process.
2. The program is designed for non-technical users and features a user-friendly GUI.
3. We provide pre-built executable files for different operating systems for easy usage.

## Installation
1. Use the pre-built executable files
   - [Windows (x86)](https://github.com/Duke-CH/role-distribution-tool/releases/latest/download/GUI_windows_x86.exe) 
   - [macOS (arm64)](https://github.com/Duke-CH/role-distribution-tool/releases/latest/download/GUI_macOS_arm64) 
2. Install the full Python repository
    ```bash
    # Clone the repository
    git clone https://github.com/Duke-CH/role-distribution-tool.git
    
    # Navigate into the directory
    cd role-distribution-tool
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Run the application
    python src/gui/GUI.py
    ```

## Usage
Please read the user guide for complete instructions on how to use the program.

## Repository Structure
```plaintext
role-distribution-tool/

├── src/
│   ├── __init__.py
│   ├── models/                 # Data models (Role, Student, etc.)
│   │   ├── __init__.py
│   │   └── role.py
│   │   └── student.py
│   ├── services/               # Business logic (role assignment, matching, etc.)
│   │   ├── __init__.py
│   │   └── role_assignment.py
│   ├── data/                   # Data access layer (DB setup, queries)
│   │   ├── db/
│   │   │   └── roles.db        # SQLite database
│   │   ├── survey_data/        # Auto-generated survey data for testing
│   │   ├── __init__.py
│   │   ├── test_data_creator.py
│   │   ├── seed.sql
│   │   └── database.py
│   ├── gui/                    # GUI layer
│   │   ├── __init__.py
│   │   ├── addRoleWindowGUI.py
│   │   ├── deleteRoleWindowGUI.sql
│   │   ├── editRoleWindowGUI.py
│   │   └── GUI.py              # Main entry point for the program
│
├── tests/                      # Unit and integration tests
│   ├── __init__.py
|   ...
│   └── test_role_assignment.py
│
├── .gitignore                  # Specifies files to ignore in version control
├── README.md                   # Project overview
```

## License
This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.