import http.server
import json
import socketserver
import urllib.parse

import base_de_donnees


PORT = 8000


base_de_donnees.initialisation()


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.request_version)
        path = urllib.parse.urlparse(self.path)

        if path.path != "/api/messages":
            self.send_error(http.HTTPStatus.NOT_FOUND)
            return

        utilisateur = self.headers["authorization"]
        
        if not utilisateur:
            self.send_error(http.HTTPStatus.UNAUTHORIZED)
            return

        query = urllib.parse.parse_qs(path.query)

        if "correspondant" not in query:
            self.send_error(http.HTTPStatus.BAD_REQUEST)
            return

        # query["correspondant"] est une liste
        # parce que en HTTP un query parameter peut être présent plusieur fois
        # exemple: "http://httpbin.org/get?test=lol&test=toto"
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


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("service en cours port", PORT)
    httpd.serve_forever()

