# Autor..........: Fernando Machado
# Data...........: 19/02/2021
# Projeto........: Pong multiplayer

from server.server import Server

HOST = "localhost"
PORT = 12000

server = Server(HOST, PORT, "test")
server.run()
