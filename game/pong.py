# Autor..........: Fernando Machado
# Data...........: 22/02/2021
# Projeto........: Pong multiplayer

import pygame

from game import Display, Player, Ball
from server import Server
from client import Client

# Controles
UP = (0, -1)
DOWM = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Pong(object):
    def __init__(self, server=1):
        """
        Jogo Pong.

        :param server: usado para teste;
        """
        self.display = Display(800, 600, "Pong")
        self.status = 0
        self.running = True

        self.server = server
        self.client = None

        self.time = 0
        self.player_1 = Player(350, 580, 200, 20, pygame.Color(255, 0, 0), self.display.get_display())
        self.player_2 = Player(350, 0, 200, 20, pygame.Color(0, 0, 255), self.display.get_display())
        self.ball = Ball(pygame.Color(255, 255, 255), self.display.get_display())

        self.clock = pygame.time.Clock()

    def run(self):
        """
        Executa Jogo.

        :return None
        """
        while self.running:
            if self.status == 0:
                self.__presentation()
            if self.status == 1:
                self.__start_menu()
            if self.status == 2:
                self.__game()

    def __presentation(self):
        """
        Animacao de apresentacao.

        :return None.
        """
        # TODO: desenvolver animacao de apresentacao
        self.status = 1

    def __start_menu(self):
        """
        Menu inicial.

        :return None.
        """
        # TODO: desenvolver menu principal
        self.status = 2

        # teste
        if self.server == 1:
            print("Cliente")
            self.server = None
            self.client = Client('127.0.0.1', 12000, self)
        elif self.server == 2:
            print("Servidor")
            self.server = Server('localhost', 12000, self)
            self.server.run()
        else:
            self.server = None
            self.server = Server('localhost', 12000, self)

    def __game(self):
        """
        Loop principal do jogo.

        :return None.
        """

        # variaveis de controle inicio
        # para manter a bola parada no inicio de cada rodada
        start_time = 50
        start_count = 0

        # variaveis de controle para tratar eventos de clique (mobile)
        clicked = False
        event_pos = 0

        playing = True

        while playing:
            self.clock.tick(60)

            # trata eventos
            # -----------------------------------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # fecha jogo
                    pygame.quit()
                    playing = False
                    self.running = False
                    break

                # trata eventos em mobile
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True
                    event_pos = event.pos
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = False

            # fecha jogo
            if not playing:
                break

            # trata movimentacao do player local
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT] or (clicked and event_pos[0] < 400):
                self.player_1.move(LEFT)
            if pressed[pygame.K_RIGHT] or (clicked and event_pos[0] > 400):
                self.player_1.move(RIGHT)

            # trata movimentacao do player 2
            if not self.client:
                if pressed[pygame.K_a]:
                    self.player_2.move(LEFT)
                if pressed[pygame.K_d]:
                    self.player_2.move(RIGHT)
            else:
                self.client.send_request()

            # -----------------------------------------------------------------------

            # transforma objetos
            # -----------------------------------------------------------------------

            # somente se a controle de inicio permite
            if start_count > start_time:

                self.ball.collide(self.player_1)
                self.ball.collide(self.player_2)
                self.ball.move()
                point = self.ball.bounce()

                if point != 0:
                    start_count = 0
                    self.ball.reset()

                    if point == 1:
                        self.player_2.set_point(1)
                    else:
                        self.player_1.set_point(1)
            else:
                start_count += 1
            # -----------------------------------------------------------------------

            # renderiza objectos
            # -----------------------------------------------------------------------
            # limpa tela (preto)
            self.display.clear_screen()

            # desenha objetos do jogo
            self.player_1.update()
            self.player_2.update()
            self.ball.update()

            # atualiza tela
            self.display.update()
            # -----------------------------------------------------------------------
