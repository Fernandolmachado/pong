# Autor..........: Fernando Machado
# Data...........: 22/02/2021
# Projeto........: Pong multiplayer

import pygame


class Player(object):
    def __init__(self, x: int, y: int, width: int, height: int, color: pygame.Color, surface: pygame.Surface):
        """
        Instancia representa objeto do manipulado pelos jogadores.

        :param x: posicao x do retangulo;
        :param y: posicao y do retangulo;
        :param width: largura do retangulo;
        :param height: altura do retangulo;
        :param color: cor do retangulo;
        :param surface: superficie onde o retangulo sera renderizado;
        """

        self.points = 0

        self.rect = pygame.Rect(x, y, width, height)

        # camadas latareis do retangulo principal, para checar colisao lateral
        self.left_rect = pygame.Rect(x, y, 1, height)
        self.right_rect = pygame.Rect(x + width - 1, y, 1, height)

        self.speed = 3
        self.color = color
        self.surface = surface

        self.moving = 0

    def move(self, controls: tuple):
        """
        Move o retangulo, conforme paramentros.

        :param controls: multiplicadores x e y da velocidade de movimentacao do player.
        :return None.
        """
        x, y = controls

        x_pos = self.rect.x
        y_pos = self.rect.y
        wid = self.rect.width
        hei = self.rect.height

        # checa colisao com as extremidas da tela
        if (x < 0 < x_pos) or x > 0 and x_pos + wid < self.surface.get_width():
            self.rect.x += (x * self.speed)
            self.moving = (x * self.speed)
        if y_pos >= 0 and y_pos + hei <= self.surface.get_height():
            self.rect.y += (y * self.speed)

        # reposiciona as camadas laterais
        self.__sides()

    def update(self):
        """
        Desenha o retangulo que representa o player.

        :return None.
        """
        self.moving = 0
        self.rect = pygame.draw.rect(
            self.surface,
            self.color,
            self.rect
        )

    def __sides(self):
        """
        Posiociona as camadas laterais.

        :return None.
        """
        self.left_rect.x = self.rect.x
        self.right_rect.x = self.rect.x + self.rect.width - 1

    # getters e setters
    def set_point(self, point: int, add=True):
        """
        Soma ou atribui pontuacao do player

        :return None
        """
        if add:
            self.points += point
        else:
            self.points = point

    def get_point(self) -> int:
        return self.points

    def set_rect(self, rect: pygame.Rect):
        self.rect = rect

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_sides(self) -> dict:
        return {"left": self.left_rect, "right": self.right_rect}

    def set_speed(self, speed: int):
        self.speed = speed

    def get_speed(self) -> int:
        return self.speed

    def set_color(self, color: int):
        self.color = color

    def get_color(self) -> pygame.Color:
        return self.color

    def set_surface(self, surface: pygame.Surface):
        self.surface = surface

    def get_surface(self) -> pygame.Surface:
        return self.surface

    def is_moving(self) -> int:
        return self.moving
