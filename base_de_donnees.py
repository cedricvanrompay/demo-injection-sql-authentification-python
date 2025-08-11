import os
import sqlite3


CHEMIN_BASE_DE_DONNEES = "base-de-donnees.db"


def initialisation():
    if os.path.isfile(CHEMIN_BASE_DE_DONNEES):
        return
    
    connection = sqlite3.connect(CHEMIN_BASE_DE_DONNEES)

    with open("init-base-de-donnees.sql") as f:
        connection.executescript(f.read())

    connection.close()


def obtenir_messages(auteur, destinataire):
    connection = sqlite3.connect(CHEMIN_BASE_DE_DONNEES)
    
    messages = list()

    requete = f"SELECT * FROM messages WHERE auteur = '{auteur}' AND destinataire = '{destinataire}'"

    print("requete: ", requete)

    for ligne in connection.execute(requete):
        date, auteur, destinataire, contenu = ligne
        messages.append({
            "date": date,
            "auteur": auteur,
            "destinataire": destinataire,
            "contenu": contenu,
        })

    connection.close()

    return messages


def mot_de_passe_utilisateur(utilisateur):
    connection = sqlite3.connect(CHEMIN_BASE_DE_DONNEES)

    requete = f"""
        SELECT mot_de_passe
        FROM utilisateurs
        WHERE pseudo = '{utilisateur}'
    """

    print("requete: ", requete)

    ligne = connection.execute(requete).fetchone()

    connection.close()

    return ligne[0]
    