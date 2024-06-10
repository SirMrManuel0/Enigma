import http.server
import logging
import json
import string
import random

from src.supply.PathsManager import PathsManager
from src.machine.Enigma import Enigma, EnigmaException
from src.machine.Rotor import Rotor, RotorException
from src.machine.Reflector import Reflector, ReflectorException

class EnigmaHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        # Setup logger
        self._logger = logging.getLogger("Handle Logger")
        self._logger.setLevel(logging.INFO)

        if not self._logger.handlers:
            fh = logging.FileHandler(
                PathsManager().getPath(PathsManager.SUPER_ID.index("Server"), PathsManager.ID.index("handle.log"))
            )
            fh.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)

            self._logger.addHandler(fh)

        self._logger.info(f"Server has connected with {client_address}")
        super().__init__(request, client_address, server)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        rotor1 = rotor2 = rotor3 = reflector = None
        error = {"RotorErr": None, "ReflectorErr": None, "EnigmaErr": None}

        try:
            rotor1 = Rotor(**data['rotor1'])
            rotor2 = Rotor(**data['rotor2'])
            rotor3 = Rotor(**data['rotor3'])
        except RotorException as e:
            error["RotorErr"] = e.__str__()
            self._logger.error(e)

        try:
            reflector = Reflector(**data['reflector'])
        except ReflectorException as e:
            error["ReflectorErr"] = e.__str__()
            self._logger.error(e)

        plugboard = data['plugboard']
        msg = data['msg']

        t = {}
        for k, v in plugboard.items():
            t[int(k)] = v
        plugboard = t
        del t

        processed_message = "Error: user input was faulty!"

        try:
            enigma = Enigma(rotor1, rotor2, rotor3, reflector, plugboard)
            if data["code"] == 0:
                processed_message = enigma.input_str(msg)
            if data["code"] == 1:
                processed_message = enigma.encrypt_wrapper(msg, data["hide_code"])
            if data["code"] == 2:
                time, length, beta_code, alpha_code, call_sign, message = enigma.decrypt_wrapper(msg)
                call_sign = ''.join(random.choices(string.ascii_uppercase, k=2)) + call_sign
                body = call_sign + message
                header = f"{time} - {len(body)} - {"".join(beta_code)} {"".join(alpha_code)} - "
                body = ' '.join([body[i:i + 5] for i in range(0, len(body), 5)])
                processed_message = header + body

        except EnigmaException as e:
            error["EnigmaErr"] = e.__str__()
            self._logger.error(e)

        response = {"encrypted_message": processed_message}
        response.update(error)
        response = json.dumps(response)

        self._logger.info(f"Client {self.client_address} has sent message {data}.")
        self._logger.info(f"Server sent to Client {self.client_address} message {response}.")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.encode())

class Server:
    def __init__(self, port: int, ip: str = ""):
        self._port = port
        self._ip = ip

        # Setup logger
        self._logger = logging.getLogger("Server Logger")
        self._logger.setLevel(logging.INFO)
        fh = logging.FileHandler(
            PathsManager().getPath(PathsManager.SUPER_ID.index("Server"), PathsManager.ID.index("server.log"))
        )
        fh.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)
        self._logger.addHandler(fh)
        self._logger.info("Server has been initiated.")

    def start(self):
        server_address = (self._ip, self._port)
        httpd = http.server.HTTPServer(server_address, EnigmaHandler)

        self._logger.info(f"Server running on '{self._ip}:{self._port}'")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
            self._logger.info("Server has been closed.")
