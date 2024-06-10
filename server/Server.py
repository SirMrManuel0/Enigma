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
        """
        This method initializes a new EnigmaHandler-Object and uses the params request, client_address, server.
        It also calls super().__init__() and creates a Handler Logger.
        :param request:
        :param client_address:
        :param server:
        """
        # Setup logger
        self._logger = logging.getLogger("Handle Logger")
        self._logger.setLevel(logging.INFO)

        if not self._logger.handlers:
            # This stops multiple useless log entries
            fh = logging.FileHandler(
                PathsManager().getPath(PathsManager.SUPER_ID.index("Server"), PathsManager.ID.index("handle.log"))
            )
            fh.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)

            self._logger.addHandler(fh)

        self._logger.info(f"Server has connected with {client_address}")
        # calling super().__init__() to make sure everything works fine
        super().__init__(request, client_address, server)

    def do_OPTIONS(self):
        """
        necessary method for the server to work...
        :return:
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-type')
        self.end_headers()

    def do_POST(self):
        """
        This method handles post request (the only request type I will use).
        It creates Rotor, Reflector and Enigma Objects according to the user input.
        :return:
        """
        # Basic data retrieval from the request.
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        # creating rotor1, rotor2, rotor3, reflector variables to prevent errors later on
        rotor1 = rotor2 = rotor3 = reflector = None
        # error dict to send errors to the website
        error = {"RotorErr": None, "ReflectorErr": None, "EnigmaErr": None}

        try:
            # creating Rotor objects
            rotor1 = Rotor(**data['rotor1'])
            rotor2 = Rotor(**data['rotor2'])
            rotor3 = Rotor(**data['rotor3'])
        except RotorException as e:
            # If there is an error, save it!
            error["RotorErr"] = e.__str__()
            self._logger.error(e)

        try:
            # creating Reflector object
            reflector = Reflector(**data['reflector'])
        except ReflectorException as e:
            # If there is an error, save it!
            error["ReflectorErr"] = e.__str__()
            self._logger.error(e)

        plugboard = data['plugboard']
        msg = data['msg']

        # make sure all keys, vals in plugboard are ints
        t = {}
        for k, v in plugboard.items():
            t[int(k)] = v
        plugboard = t
        del t

        # default error message
        processed_message = "Error: user input was faulty!"

        try:
            # create Enigma-Object
            enigma = Enigma(rotor1, rotor2, rotor3, reflector, plugboard)

            # call the correct method based on the user preference
            if data["code"] == 0:
                # standard en- and decrypting of a message using the enigma
                processed_message = enigma.input_str(msg)
            if data["code"] == 1:
                # encrypt according to WW2 germany regulations
                processed_message = enigma.encrypt_wrapper(msg, data["hide_code"])
            if data["code"] == 2:
                # decrypt according to WW2 germany regulations
                time, length, beta_code, alpha_code, call_sign, message = enigma.decrypt_wrapper(msg)
                call_sign = ''.join(random.choices(string.ascii_uppercase, k=2)) + call_sign
                body = call_sign + message
                header = f"{time} - {len(body)} - {"".join(beta_code)} {"".join(alpha_code)} - "
                body = ' '.join([body[i:i + 5] for i in range(0, len(body), 5)])
                processed_message = header + body

        except EnigmaException as e:
            # Catch error and save it
            error["EnigmaErr"] = e.__str__()
            self._logger.error(e)

        # wrap the response up
        response = {"encrypted_message": processed_message}
        response.update(error)
        response = json.dumps(response)

        # send it
        self._logger.info(f"Client {self.client_address} has sent message {data}.")
        self._logger.info(f"Server sent to Client {self.client_address} message {response}.")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.encode())

class Server:
    def __init__(self, port: int, ip: str = ""):
        """
        This method initializes a new Server-Object with a port as int and an ip as str.
        It also creates the Server Logger.
        :param port:
        :param ip:
        """
        # Set port and ip
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
        """
        This method starts the server and sets the EnigmaHandler.
        :return:
        """
        server_address = (self._ip, self._port)
        httpd = http.server.HTTPServer(server_address, EnigmaHandler)

        self._logger.info(f"Server running on '{self._ip}:{self._port}'")
        try:
            # Server will run until forcefully shut off | through e.g. KeyboardInterrupt
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
            self._logger.info("Server has been closed.")
