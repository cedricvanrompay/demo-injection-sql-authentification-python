import http.server
import json
import socketserver
import urllib.parse

import authentification
import base_de_donnees


PORT = 8000

CHEMIN_FICHIERS_STATIQUES = "fichiers-statiques"


base_de_donnees.initialisation()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args):
        super().__init__(*args, directory=CHEMIN_FICHIERS_STATIQUES)

    def do_POST(self):
        path = urllib.parse.urlparse(self.path)

        if path.path == "/authentification":
            content_length = int(self.headers.get('Content-Length', 0))
            set_cookie = authentification.traiter_requete_connection(self.rfile.read(content_length))

            if not set_cookie:
                self.send_error(http.HTTPStatus.UNAUTHORIZED)
                return

            self.send_response(http.HTTPStatus.FOUND)
            self.send_header("Set-Cookie", set_cookie)
            self.send_header("Location", "/messagerie.html")
            self.send_header("Content-Length", "0")
            self.end_headers()

        else:
            self.send_error(http.HTTPStatus.NOT_FOUND)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(path.query)

        if path.path == "/api/messages":
            self.liste_messages(query)
        elif path.path == "/api/utilisateurs":
            self.liste_utilisateurs(query)
        else:
            super().do_GET()

    def liste_messages(self, query):
        utilisateur = authentification.authentifier_headers(self.headers["cookie"])
        
        if not utilisateur:
            self.send_error(http.HTTPStatus.UNAUTHORIZED)
            return

        if "correspondant" not in query:
            self.send_error(http.HTTPStatus.BAD_REQUEST)
            return

        correspondant = query["correspondant"][0]

        messages = base_de_donnees.obtenir_messages(
            auteur=utilisateur,
            destinataire=correspondant,
        )

        messages = messages + base_de_donnees.obtenir_messages(
            auteur=correspondant,
            destinataire=utilisateur,
        )

        messages.sort(key=lambda a: a["date"])


        self.send_response(http.HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        corps_reponse = json.dumps(messages, indent=4, ensure_ascii=False)
        
        self.wfile.write(corps_reponse.encode())

    def liste_utilisateurs(self, query):
        pseudo = query["pseudo"][0]

        utilisateurs = base_de_donnees.trouver_utilisateur(pseudo)
        
        self.send_response(http.HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        corps_reponse = json.dumps(utilisateurs, indent=4, ensure_ascii=False)
        
        self.wfile.write(corps_reponse.encode())


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


with ReusableTCPServer(("", PORT), Handler) as httpd:
    print(f"service en cours à l'addresse http://localhost:{PORT}")
    httpd.serve_forever()

