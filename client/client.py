# Autor..........: Fernando Machado
# Data...........: 19/02/2021
# Projeto........: Pong multiplayer

import socket
import json

from server import Protocol


class Client(object):
    def __init__(self, host: str, port: int, app):
        """
        Cria socket com protocolo TCP para jogar Pong em Lan

        :param host: ip do servidor que irá se conectar.
        :param port: porta de acesso ao servidor.
        :param app: instancia da classe Pong (jogo).
        """
        self.host = host
        self.port = port
        self.app = app
        self.address = (self.host, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__connect()

    def send_request(self, code=1):
        """
        Envia dados ao servidor de acordo com o codigo definido no protocolo de comunicacao.

        :param code: code do protocolo (server.Protocol).
        :return None
        """
        if code == 1:
            # cria requisicao
            request = Protocol.get
            request["request"]["data"]["x_position"] = self.app.player_1.get_rect().x
            request["request"]["data"]["y_position"] = self.app.player_1.get_rect().y

            # envia requisicao ao servidor
            request = json.dumps(request)
            self.socket.sendall(request.encode())

            # recebe resposta
            response = self.__get_response()
            response = json.loads(response)

            # atribui pontos do jogador cliente
            self.app.player_1.set_point(response["response"]["data"]["player_2"]["points"], add=False)

            # trata dados do jogador servidor
            player_rect = self.app.player_2.get_rect()
            player_rect.x = response["response"]["data"]["player_1"]["x_position"]
            # player_rect.y = response["response"]["data"]["player_1"]["y_position"]
            self.app.player_2.set_rect(player_rect)
            self.app.player_2.set_point(response["response"]["data"]["player_1"]["points"], add=False)

            # trata dados do jogo
            self.app.ball.set_center(response["response"]["data"]["game"]["ball_position"])
            self.app.time = response["response"]["data"]["game"]["time"]

        elif code == 8:
            # TODO: Desenvolver protocolo 8
            raise NotImplementedError()

        elif code == 9:
            request = json.dumps(Protocol.close)
            self.socket.sendall(request.encode())

    def __connect(self):
        """
        Conecta ao servidor de acordo com os dados passados na instancia.

        :return: None.
        """
        self.socket.connect(self.address)

    def __get_response(self) -> str:
        """
        Recebe retorno do servidor.

        :return (str) dados de retorno
        """
        return self.socket.recv(1024).decode()
