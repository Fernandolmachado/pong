# Autor..........: Fernando Machado
# Data...........: 19/02/2021
# Projeto........: Pong multiplayer

import socket
import threading
import json

from server import Log


class Server(object):
    def __init__(self, host: str, port: int, app):
        """
        Cria socket com protocolo TCP para jogar Pong em Lan

        :param host: ip do servidor.
        :param port: porta de acesso.
        :param app: instancia da classe Pong (jogo).
        """
        self.host = host
        self.port = port
        self.address = (self.host, self.port)
        self.app = app
        self.connection = None
        self.__configure()

    def run(self):
        """
        Escuta por conexoes e aceita. Cria thread para manter comunicacao.

        :return: None.
        """
        self.socket.listen()
        Log.print("waiting connection...", type_cod=1)
        self.__accept_connection()
        communication = threading.Thread(target=self.__communicate)
        communication.start()

    def __configure(self):
        """
        Configura socket.

        :return: None.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        Log.print("initializing server...", type_cod=1)

    def __accept_connection(self):
        """
        Aceita conexao

        :return: None.
        """
        connection, address = self.socket.accept()

        self.connection = {
            "connection": connection,
            "address": address
        }

        Log.print("Connected: " + str(address), type_cod=1)

    def __communicate(self):
        """
        Mantem comunicacao com cliente.

        :return: None.
        """
        connection = self.connection["connection"]
        address = self.connection["address"]

        Log.print("establishing communication...", type_cod=1)
        while True:
            data = connection.recv(1024).decode()
            Log.print("Request received: " + str(address))
            self.__handle_request(json.loads(data))

    def __handle_request(self, data: dict):
        """
        Trata requisicoes de acordo com codigo definido no protocolo.

        :param data: informacao recebido do cliente.
        :return: None.
        """
        connection = self.connection["connection"]
        address = self.connection["address"]

        if data["request"]["code"] == 1:
            # requisicao de atualizacao do jogo
            player_2_pos_x = data["request"]["data"]["x_position"]
            player_2_pos_y = data["request"]["data"]["y_position"]

            player_1 = data["response"]["data"]["player_1"]
            player_2 = data["response"]["data"]["player_2"]
            game = data["response"]["data"]["game"]

            # monta resposta
            # dados do jogador servidor
            player_1["x_position"] = self.app.player_1.get_rect().x
            player_1["y_position"] = self.app.player_1.get_rect().y
            player_1["points"] = self.app.player_1.get_point()
            data["response"]["data"]["player_1"] = player_1

            # dados do jogador cliente
            player_2["x_position"] = player_2_pos_x
            player_2["y_position"] = player_2_pos_y
            player_2["points"] = self.app.player_2.get_point()
            data["response"]["data"]["player_2"] = player_2

            # dados do jogo
            # TODO: criar algoritmo do tempo
            game["time"] = 0
            ball = self.app.ball.get_center().copy()
            ball[1] = self.app.display.get_display().get_rect().height - ball[1]
            game["ball_position"] = ball
            data["response"]["data"]["game"] = game

            # atualiza dados do jogador cliente no jogo
            player_rect = self.app.player_2.get_rect()
            player_rect.x = player_2_pos_x
            self.app.player_2.set_rect(player_rect)

            # envia resposta
            data = json.dumps(data)
            self.connection["connection"].sendall(data.encode())

        elif data["request"]["code"] == 8:
            # TODO: desenvolver tratamento do protocolo 8
            raise NotImplementedError()

        elif data["request"]["code"] == 9:
            # fecha conexao a pedido do cliente
            # TODO: criar algoritmo para fechar conexao a pedido do servidor
            connection["connection"].close()
            Log.print("Connection closed: " + str(address), type_cod=1)
            self.connection = None

        else:
            # TODO: desenvolver algoritmo de protocolo desconhecido
            Log.print("Unknown code: " + str(data["request"]["code"]), type_cod=3)
            raise NotImplementedError()
