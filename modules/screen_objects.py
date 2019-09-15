import pygame
import pygame.gfxdraw
from modules.config import *


class Button(object):
    def __init__(self, text, posX=100, posY=100, width=50, height=30):
        self.width = width
        self.height = height
        self.posX = posX
        self.posY = posY
        self.box = pygame.Rect(self.posX, self.posY, self.width, self.height)
        self.font = pygame.font.Font(None, 32)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = text
        self.done = False

    def set_colors(self, color_active, color_inactive):
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.color = self.color_inactive

    def set_font_size(self, size):
        self.font = pygame.font.Font(None, size)

    def set_pos(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.box = pygame.Rect(self.posX, self.posY, self.width, self.height)

    def draw(self, screen):
        txt_surface = self.font.render(
            self.text, True, self.color)
        width = max(self.width, txt_surface.get_width()+10)
        self.box.w = width
        screen.blit(txt_surface, (self.box.x +
                                  5, self.box.y+5))
        pygame.draw.rect(screen, self.color,
                         self.box, 2)

    def clicked(self):
        self.active = not self.active
        self.switch_status()

    def switch_status(self):
        self.color = self.color_active if self.active else self.color_inactive


class Input(Button):
    def __init__(self, posX=100, posY=100, width=50, height=30):
        self.width = width
        self.height = height
        self.box = pygame.Rect(posX, posY, self.width, self.height)
        self.font = pygame.font.Font(None, 32)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.done = False

    def typing(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += event.unicode
