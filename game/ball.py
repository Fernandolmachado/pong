# Autor..........: Fernando Machado
# Data...........: 22/02/2021
# Projeto........: Pong multiplayer

import pygame
import random
import os

from game import Player


class Ball(object):
    def __init__(self, color: pygame.Color, surface: pygame.Surface):
        """
        A instancia representa o objeto bola do jogo Pong.

        :param color: cor da bola do jogo
        :param surface: superficie onde a bola sera renderizada
        """

        # implementar efeitos sonoros
        self.color = color
        self.surface = surface

        self.radius = 10
        self.center = None
        self.speed = None
        self.ball = None

        dirname = os.path.dirname(__file__)
        dirname = dirname.replace(r"\pong\game", r"\pong")
        filename = os.path.join(dirname, r"resources\bounce.wav")
        print(filename)

        self.bounce_sound = pygame.mixer.Sound(filename)

        self.reset()
        self.update()

    def reset(self):
        """
        Restaura posicao e velocidade padroes da bola

        :return None
        """
        self.center = list(self.surface.get_rect().center)
        self.speed = [random.choice([-3, 3]), random.choice([-3, 3])]

    def collide(self, player: Player):
        """
        Trata collisao e reacao da bola.

        :param player: objeto player, o qual sera checado a colisao
        :return None
        """

        # TODO: resolver bug de colisao lateral

        # Se nao houver colisao, retorna
        if not self.ball.colliderect(player.get_rect()):
            return

        # caso houver colisao, muda sentido de movimento da bola em y
        self.speed[1] *= -1

        # velocidade padrao
        std_sp = 4

        # pega rects laterais do objeto player
        player_sides = player.get_sides()

        # caso haja colisao na lateral esquerda
        if self.ball.colliderect(player_sides["left"]):
            if self.speed[0] > 0:
                self.speed[0] *= -1
            if self.ball.collidepoint((player_sides["left"].x,player_sides["left"].y)):
                self.speed[0] = std_sp if (self.speed[0] > 0) else -std_sp
                self.speed[1] = std_sp if (self.speed[1] > 0) else -std_sp
            else:
                self.speed[0] = (std_sp + 1) if (self.speed[0] > 0) else -(std_sp + 1)
                self.speed[1] = (std_sp - 1) if (self.speed[1] > 0) else -(std_sp - 1)

        # caso haja colisao lateral direita
        elif self.ball.colliderect(player_sides["right"]):
            if self.speed[0] < 0:
                self.speed[0] *= -1
            if self.ball.collidepoint((player_sides["right"].x,player_sides["right"].y)):
                self.speed[0] = std_sp if (self.speed[0] > 0) else -std_sp
                self.speed[1] = std_sp if (self.speed[1] > 0) else -std_sp
            else:
                self.speed[0] = (std_sp + 1) if (self.speed[0] > 0) else -(std_sp + 1)
                self.speed[1] = (std_sp - 1) if (self.speed[1] > 0) else -(std_sp - 1)

        # caso haja colisao frontal e player esta em movimento
        else:
            player_moving = player.is_moving()

            if player_moving != 0:
                if ((player_moving > 0) and (self.speed[0] < 0)) or ((player_moving < 0) and (self.speed[0] > 0)):
                    self.speed[0] *= -1
                else:
                    self.speed[0] = std_sp if (self.speed[0] > 0) else -std_sp
                    self.speed[1] = std_sp if (self.speed[1] > 0) else -std_sp

        self.bounce_sound.play()

    def move(self):
        """
        Move centro do player, conforme parametros de velocidade

        :return None
        """
        self.center[0] += self.speed[0]
        self.center[1] += self.speed[1]

    def bounce(self) -> int:
        """
        Trata collisao da bola com as extremidades do jogo.

        :return
            0 - se atingiu extremidades laterais;
            1 - se atingiu extremidade inferior;
            2 - se atingiu extremidade superior.
        """
        if self.center[0] + self.radius >= self.surface.get_width() \
                or self.center[0] - self.radius <= 0:

            self.speed[0] *= -1

        if self.center[1] + self.radius >= self.surface.get_height():
            return 1
        elif self.center[1] - self.radius <= 0:
            return 2

        return 0

    def update(self):
        """
        Desenha bola na superficie.

        :return None.
        """
        self.ball = pygame.draw.circle(self.surface, self.color, self.center, self.radius)

    # getters e setters
    def set_center(self, center):
        self.center = center

    def get_center(self) -> list:
        return self.center

    def set_speed(self, sp_x: int, sp_y: int):
        self.speed = [sp_x, sp_y]

    def get_speed(self) -> list:
        return self.speed

    def set_radius(self, radius):
        self.radius = radius

    def get_radius(self) -> int:
        return self.radius

    def set_color(self, color: pygame.Color):
        self.color = color

    def get_color(self) -> pygame.Color:
        return self.color

    def set_surface(self, surface: pygame.Surface):
        self.surface = surface

    def get_surface(self) -> pygame.Surface:
        return self.surface

    def get_rect(self) -> pygame.Rect:
        return self.ball
