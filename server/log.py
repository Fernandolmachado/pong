# Autor..........: Fernando Machado
# Data...........: 22/02/2021
# Projeto........: Pong multiplayer

from datetime import date


class Log(object):

    @staticmethod
    def print(msg: str, type_cod=1):
        """
        Escreve log formatado no terminal do servidor.

        :param msg: Mensagem a ser escrita no terminal;
        :param type_cod: Tipo da mensagem
        :return: None.
        """
        if type_cod == 1:
            type = "[Information]"
        elif type_cod == 2:
            type = "[Warning]"
        elif type_cod == 3:
            type = "[Error]"

        today = date.today()

        print(str(today) + ": " + type + " " + msg)
