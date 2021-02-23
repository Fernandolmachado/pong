# Autor..........: Fernando Machado
# Data...........: 19/02/2021
# Projeto........: Pong multiplayer

from client import Client

HOST = "127.0.0.1"
PORT = 12000

c = Client(HOST, PORT, "test")
while True:
    c.send_request(input("msg: "))
    print(c.get_response())
