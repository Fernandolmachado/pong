# Autor..........: Fernando Machado
# Data...........: 22/02/2021
# Projeto........: Pong multiplayer

class Protocol(object):
    """
    Contêm dicionarios com estrura de dados por protocolo
    """
    # envia posicao do jogador (cliente) e recebe dados do jogo
    get = {
        "request": {
            "code": 1,
            "data": {
                "x_position": None,
                "y_position": None
            }
        },
        "response": {
            "code": 1,
            "data": {
                "player_1": {
                    "x_position": None,
                    "y_position": None,
                    "points": None
                },
                "player_2": {
                    "x_position": None,
                    "y_position": None,
                    "points": None
                },
                "game": {
                    "time": None,
                    "ball_position": None
                }
            }
        }
    }

    # solicita pause do jogo
    pause = {
        "request": {
            "code": 8,
        },
        "response": {
            "code": 8,
            "data": True or False
        }
    }

    # fecha conexao
    close = {
        "request": {
            "code": 9,
        },
        "response": {
            "code": 9,
            "data": True or False
        }
    }