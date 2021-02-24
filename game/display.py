# Autor..........: Fernando Machado
# Data...........: 22/02/2021
# Projeto........: Pong multiplayer

import pygame


class Display(object):
    def __init__(self, width: int, height: int, title: str):
        """
        Instancia representa objeto da janela.

        :param width: largura da janela;
        :param height: altura do janela;
        :param title: Titulo apresentado na janela;
        """
        self.width = width
        self.heigth = height
        
        self.display = pygame.display.set_mode((self.width, self.heigth))
        pygame.display.set_caption(title)
        
    def get_display(self) -> pygame.Surface:
        """
        Retorna janela.

        :return: superficie da janela.
        """
        return self.display
    
    def clear_screen(self):
        """
        Limpa tela com cor preto.

        :return None
        """
        self.display.fill(0x000000)
        
    def update(self):
        """
        Atualiza tela.

        :return None
        """
        pygame.display.update()
