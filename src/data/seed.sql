PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

-- Drop tables if they already exist to avoid errors
DROP TABLE IF EXISTS Roles;
DROP TABLE IF EXISTS SpecialGroups;

-- Create Roles table with auto-increment primary key
CREATE TABLE Roles (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- Artificial ID
        Vorname_Position TEXT,
        Nachname TEXT,
        Rollengruppe TEXT,
        Gender TEXT,
        Essential_Next_Rest_Last TEXT,
        just_8b TEXT,
        Thema TEXT,
        Soziale_Beziehungen INTEGER
    );

-- Create SpecialGroups table
CREATE TABLE SpecialGroups (
    GroupID INTEGER PRIMARY KEY  -- Unique group identifier
);

-- Insert data into Roles
INSERT INTO Roles VALUES(NULL, 'Kris','Anpu','Klasse 8a','Unisex','Rest','','Diversität/Rassismus/Diskriminerung (Gerechtigkeit)',1);
INSERT INTO Roles VALUES(NULL, 'Sophia','Apeiro','Klasse 8a','Weiblich','Rest','','Lernschwierigkeiten/Inklusion (Strukturen im Unterricht wichtig)',2);
INSERT INTO Roles VALUES(NULL, 'Cem','Ask','Klasse 8a','Männlich','Essential','','Diversität/Rassismus/Diskriminierung (Migrationshintergrund) ',3);
INSERT INTO Roles VALUES(NULL, 'Amar','Fürst','Klasse 8a','Unisex','Rest','','',0);
INSERT INTO Roles VALUES(NULL, 'David','Herbst','Klasse 8a','Männlich','Rest','','',0);
INSERT INTO Roles VALUES(NULL, 'Lotte','Hermann','Klasse 8a','Weiblich','Rest','','Inklusion/Diversität (mehrfache Klassenwiederholung)',0);
INSERT INTO Roles VALUES(NULL, 'Toni','Klein','Klasse 8a','Unisex','Essential','','Inklusion/Diversität (psychisch belastet)',2);
INSERT INTO Roles VALUES(NULL, 'Erwin','Koch','Klasse 8a','Männlich','Next','','Diversität/Rassismus/Diskriminerung (Streitschlichter, Barrierefreiheit)',0);
INSERT INTO Roles VALUES(NULL, 'Jona','Lautner','Klasse 8a','Unisex','Essential','','',4);
INSERT INTO Roles VALUES(NULL, 'Julius','Mair','Klasse 8a','Männlich','Essential','','',2);
INSERT INTO Roles VALUES(NULL, 'Hannah','Mittermeier','Klasse 8a','Weiblich','Next','','Inklusion/Diversität (psychisch (familiär) belastet)',1);
INSERT INTO Roles VALUES(NULL, 'Leo','Müller','Klasse 8a','Männlich','Essential','','Inklusion/Diversität (psychisch (familiär) belastet)',2);
INSERT INTO Roles VALUES(NULL, 'Felipe','Nube','Klasse 8a','Männlich','Rest','','Lernschwierigkeiten/Inklusion (schriftliche Leistungen schwach)',0);
INSERT INTO Roles VALUES(NULL, 'Ava','Rittersprung','Klasse 8a','Weiblich','Essential','','Lernschwierigkeiten/Inklusion (Leserechtschreibschwäche, Abschaffen von Noten)',3);
INSERT INTO Roles VALUES(NULL, 'Ailyn (Kim)','Sering','Klasse 8a','Divers','Essential','','Diversität/Rassismus/Diskriminerung (Non-Binär)',5);
INSERT INTO Roles VALUES(NULL, 'Luca','Schmidt','Klasse 8a','Unisex','Next','','Lernschwierigkeiten/Inklusion (Aufmerksamkeitsprobleme, Bewegungsbedürfnis)',2);
INSERT INTO Roles VALUES(NULL, 'Leonie','Wagner','Klasse 8a','Weiblich','Essential','','Nachhaltigkeit',1);
INSERT INTO Roles VALUES(NULL, 'Nayk','Zena','Klasse 8a','Männlich','Rest','','',0);
INSERT INTO Roles VALUES(NULL, 'Kara','Beil','Klasse 8b','Weiblich','Essential','yes','',6);
INSERT INTO Roles VALUES(NULL, 'Flo','Christmann','Klasse 8b','Unisex','Rest','','',0);
INSERT INTO Roles VALUES(NULL, 'Alex','Domstoll','Klasse 8b','Unisex','Rest','','Diversität/Inklusion (psychisches Problem)',0);
INSERT INTO Roles VALUES(NULL, 'Johannes','Frieden','Klasse 8b','Männlich','Essential','yes','Diversität/Inklusion (Hochbegabung)',0);
INSERT INTO Roles VALUES(NULL, 'Elena','Hanke','Klasse 8b','Weiblich','Rest','','Antirassismus (Mehrsprachigkeit)',7);
INSERT INTO Roles VALUES(NULL, 'Leon','Huber','Klasse 8b','Männlich','Essential','yes','Diversität/Inklusion (Lernschwäche)',8);
INSERT INTO Roles VALUES(NULL, 'Maria','Jung','Klasse 8b','Weiblich','Next','','Zuhause Notenrelevanz, Schulhund',9);
INSERT INTO Roles VALUES(NULL, 'Sina','Knopf','Klasse 8b','Weiblich','Essential','yes','Diversität/Inklusion (Herzschrittmacher)',9);
INSERT INTO Roles VALUES(NULL, 'Max','Krüger','Klasse 8b','Männlich','Essential','yes','',8);
INSERT INTO Roles VALUES(NULL, 'Issa','Linda','Klasse 8b','Unisex','Essential','yes','',6);
INSERT INTO Roles VALUES(NULL, 'Wanja','Liu','Klasse 8b','Unisex','Next','','Diversität/Diskriminierung (Rassismus)',0);
INSERT INTO Roles VALUES(NULL, 'Yagmur','Metiner','Klasse 8b','Männlich','Essential','yes','Diversität/Inklusion (Farbenblindheit)',9);
INSERT INTO Roles VALUES(NULL, 'Martin','Musalaha','Klasse 8b','Männlich','Essential','yes','Nachhaltigkeit',9);
INSERT INTO Roles VALUES(NULL, 'Kamil','Pirog','Klasse 8b','Männlich','Rest','','Macho, Antirassismus',7);
INSERT INTO Roles VALUES(NULL, 'Josephine','Schubert','Klasse 8b','Weiblich','Rest','','',7);
INSERT INTO Roles VALUES(NULL, 'Mike','Sreca','Klasse 8b','Männlich','Next','','',0);
INSERT INTO Roles VALUES(NULL, 'Bente','Stumpf','Klasse 8b','Unisex','Essential','yes','eventuell: Diversität/Inklusion (ADHS)',9);
INSERT INTO Roles VALUES(NULL, 'Lilli','Unhoch','Klasse 8b','Weiblich','Essential','yes','',0);
INSERT INTO Roles VALUES(NULL, 'Förderschullehrkraft','Deghan','Lehrkraft/Schulpersonal','Unisex','Essential','yes','',1000);
INSERT INTO Roles VALUES(NULL, 'Lehrkraft','Alidoust','Lehrkraft/Schulpersonal','Unisex','Essential','yes','',1000);
INSERT INTO Roles VALUES(NULL, 'Lehrkraft','Amara','Lehrkraft/Schulpersonal','Unisex','Essential','yes','',1000);
INSERT INTO Roles VALUES(NULL, 'Lehrkraft','Böhmer','Lehrkraft/Schulpersonal','Unisex','Essential','yes','',1000);
INSERT INTO Roles VALUES(NULL, 'Lehrkraft','Emminger','Lehrkraft/Schulpersonal','Unisex','Essential','no','',1000);
INSERT INTO Roles VALUES(NULL, 'Lehrkraft','Hans-Meric','Lehrkraft/Schulpersonal','Unisex','Essential','no','',1000);
INSERT INTO Roles VALUES(NULL, 'Lehrkraft im Vorbereitungsdienst','Park','Lehrkraft/Schulpersonal','Unisex','Next','next','',1000);
INSERT INTO Roles VALUES(NULL, 'Lehrkraft','Zöpfel','Lehrkraft/Schulpersonal','Unisex','Essential','yes','',1000);
INSERT INTO Roles VALUES(NULL, 'Schulleitung von','Buchtahl','Lehrkraft/Schulpersonal','Unisex','Next','','',1000);
INSERT INTO Roles VALUES(NULL, 'Schulsozialarbeit','Adeyemi','Lehrkraft/Schulpersonal','Unisex','Next','','',1000);
INSERT INTO Roles VALUES(NULL, 'Sekretariat','Meyer-Sehring','Lehrkraft/Schulpersonal','Unisex','Last','no','',1000);

-- Insert data into SpecialGroups
INSERT INTO SpecialGroups VALUES(7);

COMMIT;
