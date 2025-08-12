-- tables

CREATE TABLE utilisateurs (
    pseudo TEXT PRIMARY KEY NOT NULL,
    mot_de_passe TEXT NOT NULL,
    date_creation DATETIME NOT NULL
);

CREATE TABLE messages (
    date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    auteur TEXT NOT NULL REFERENCES utilisateurs(pseudo),
    destinataire TEXT NOT NULL REFERENCES utilisateurs(pseudo),
    contenu TEXT NOT NULL,
    PRIMARY KEY (date, auteur, destinataire)
);


-- données de test

INSERT INTO utilisateurs(pseudo, mot_de_passe, date_creation) VALUES
    ("alice", "123test", "2025-05-06 10:00:00"),
    ("bob", "456test", "2025-05-08 15:00:00"),
    ("charlie", "789test", "2025-05-09 11:00:00")
;

INSERT INTO messages VALUES('2025-08-09 08:00:14','alice','bob','bonjour');
INSERT INTO messages VALUES('2025-08-09 08:00:29','bob','alice','salut');
INSERT INTO messages VALUES('2025-08-09 08:00:47','alice','bob','ça va ?');
INSERT INTO messages VALUES('2025-08-09 08:01:01','bob','alice','oui et toi ?');
INSERT INTO messages VALUES('2025-08-09 08:01:19','charlie','bob','hello');
INSERT INTO messages VALUES('2025-08-09 08:01:32','bob','charlie','hello :-)');
INSERT INTO messages VALUES('2025-08-09 08:01:43','charlie','bob','comment tu vas ?');