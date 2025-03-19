import csv
import random

def generate_test_data(output_file, num_rows, empty_percentage):
    # Column headers
    headers = [
        "Antwort ID",
        "Datum Abgeschickt",
        "Letzte Seite",
        "Start-Sprache",
        "Zufallsstartwert",
        "Geben Sie ihren Vor- und Nachnamen an. [Vorname]",
        "Geben Sie ihren Vor- und Nachnamen an. [Nachname]",
        "Welches Geschlecht schreiben Sie sich selbst zu?",
        "Gibt es ein Geschlecht, das Sie auf keine Fall spielen wollen?"
    ]

    # Gender options
    gender_options = ["Männlich", "Weiblich", "Divers"]
    avoid_gender_options = ["Männlich", "Weiblich", "Divers", ""]

    # Calculate the number of empty values for the ninth column
    num_empty = int(num_rows * empty_percentage / 100)
    avoid_gender_values = ["" for _ in range(num_empty)] + [
        random.choice([g for g in avoid_gender_options if g != ""]) for _ in range(num_rows - num_empty)
    ]
    random.shuffle(avoid_gender_values)

    # Generate rows
    data = []
    for i in range(1, num_rows + 1):
        row = [
            str(i),  # ID
            "1980-01-01 00:00:00",  # Submit date
            "1",  # Last page
            "de",  # Start language
            str(random.randint(100000000, 999999999)),  # Seed
            f"Vorname_{i}",  # First name
            f"Nachname_{i}",  # Last name
            random.choice(gender_options),  # Gender
            avoid_gender_values[i - 1]  # Avoid gender
        ]
        data.append(row)

    # Write to CSV file
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

# Automatic generation loop
for i in range(50):
    num_rows = random.randint(10, 50)
    empty_percentage = random.randint(30, 100)
    file_name = f"test_data_{num_rows}_rows_{empty_percentage}%_no_exclusion.csv"
    generate_test_data(file_name, num_rows, empty_percentage)
