import pygame
from random import randint

class Pipe :
    def __init__(self, velocity):
        self.pipe_up =  pygame.image.load('pipeup.png').convert_alpha() 
        self.pipe_down = pygame.image.load('pipedown.png').convert_alpha()
        self.rect_up = self.pipe_up.get_rect()
        self.rect_down = self.pipe_down.get_rect()
        self.pipe_dist = 110
        self.rect_up.y = randint(200, 400)
        self.rect_up.x = 350
        self.rect_down.y = self.rect_up.y - self.pipe_dist - self.rect_up.height 
        self.rect_down.x = 350
        self.velocity = velocity

    def drawPipe(self, display):
        display.blit(self.pipe_up, self.rect_up)
        display.blit(self.pipe_down, self.rect_down)

    def update(self, dt):
        self.rect_up.x -= int(self.velocity * dt)
        self.rect_down.x -= int(self.velocity * dt)