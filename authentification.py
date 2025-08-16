import base64
import datetime
import os
import urllib.parse
import http.cookies

import base_de_donnees

AGE_MAX_SESSION_JOURS = 60


sessions_par_id = dict()


def traiter_requete_connection(donnees: bytes):
    formulaire = urllib.parse.parse_qs(donnees.decode())

    utilisateur = formulaire["utilisateur"][0]

    mot_de_passe = formulaire["mot_de_passe"][0]

    attendu = base_de_donnees.mot_de_passe_utilisateur(utilisateur)

    if mot_de_passe != attendu:
        return None

    id_session = base64.b64encode(os.urandom(16)).decode()

    sessions_par_id[id_session] = {
        "utilisateur": utilisateur,
        "timestamp": datetime.datetime.now(),
    }

    return f"session={id_session}"


def authentifier_headers(cookies):
    c = http.cookies.SimpleCookie()
    c.load(cookies)

    cookie = c.get("session", None)

    if not cookie:
        return None
    
    id_session = cookie.value

    if not id_session:
        return None
    
    session = sessions_par_id[id_session]

    age = datetime.datetime.now() - session["timestamp"]

    if age.days > AGE_MAX_SESSION_JOURS:
        return None

    return session["utilisateur"]



