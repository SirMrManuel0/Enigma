import socket
import webbrowser
import os

from server.Server import Server
from supply.PathsManager import PathsManager

def clear_console():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix-like systems
    else:
        os.system('clear')

def start_web(ip: str) -> None:
    with open(PathsManager().getPath(PathsManager.SUPER_ID.index("Main"), PathsManager.ID.index("global.js")),
              "r") as f:
        lines = f.readlines()
        lines[0] = f'const IP = "{ip}";\n'
    with open(PathsManager().getPath(PathsManager.SUPER_ID.index("Main"), PathsManager.ID.index("global.js")),
              "w") as f:
        for line in lines:
            f.write(line)

    url = f"file://{os.path.realpath('user_interface/index.html')}"
    webbrowser.open_new_tab(url)


def client():
    t = ""
    while len(t) < 5:
        t = input("Please enter the server IP: ")
    con = (t, 8000)
    sock = socket.socket()
    result = sock.connect_ex(con)
    if result != 0:
        print(f"Due to connection errors to the server {con}, the server will be hosted locally.")
        input('Press Enter to continue...')
        start_web("127.0.0.1")
        server = Server(8000, ip="127.0.0.1")
        server.start()
    else:
        start_web(t)


def only_server():
    print("The server will be hosted on the port 8000.")
    print("It will listen to all ips of this device.")
    input("Press Enter to continue...")
    server = Server(8000)
    server.start()


def server_and_client():
    print("The server will be hosted on the port '8000' with the ip '127.0.0.1'.")
    print("A client will be created and connected to the local server.")
    input("Press enter to continue...")
    start_web("127.0.0.1")
    server = Server(8000, ip="127.0.0.1")
    server.start()


user_input = ""
choices = ["server", "server and client", "client"]

while user_input not in choices:
    clear_console()
    print("Enter 'server' to only host the server.")
    print("Enter 'client' to only be a client (in case of an invalid server: a server will be hosted locally)")
    print("Enter 'server and client' to host the server and be a client of it.")
    user_input = input("Enter one: ")
    user_input = user_input.lower()

if user_input == choices[0]:
    only_server()
if user_input == choices[1]:
    server_and_client()
if user_input == choices[2]:
    client()
