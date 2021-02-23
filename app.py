# Autor..........: Fernando Machado
# Data...........: 22/02/2021
# Projeto........: Pong multiplayer

import sys
from game import Pong

args = sys.argv

if len(args) == 2:
    if args[1] == '1':
        app = Pong()
    elif args[1] == '2':
        app = Pong(server=2)
else:
    app = Pong(server=0)

app.run()
