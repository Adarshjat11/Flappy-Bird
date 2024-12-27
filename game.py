import pygame
import sys, time
from Bird import Bird
from pipe import Pipe
import random

pygame.init()

class Game():
    def __init__(self):
        self.width = 350
        self.height = 550
        self.scale_factor = 1.5
        self.display = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.velocity = 150
        self.bird = Bird()
        self.enter_pressed = False
        self.startMonitoring = False  # Initialize startMonitoring to False
        self.gameStarted = True
        self.score = 0
        self.font = pygame.font.Font("font.ttf", 22)
        self.score_text = self.font.render("0", True, (0,0,0))  # Initialize score_text
        self.score_text_rect = self.score_text.get_rect(center = (170, 50))
        self.restart_text = self.font.render("Restart", True, (0,0,0))
        self.restart_text_rect = self.restart_text.get_rect(center = (175, 500))
        self.pipes = []
        self.pipe_generator = 0
        self.setUpbgandg()

        self.gameLoop()

    def gameLoop(self):
        last_time = time.time()
        while (True):
            #Calculating delta time
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and self.gameStarted: 
                    if event.key == pygame.K_RETURN :
                        self.enter_pressed = True
                        self.bird.update_on = True
                    if event.key == pygame.K_SPACE and self.enter_pressed == True :
                        self.bird.flap(dt)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_text_rect.collidepoint(pygame.mouse.get_pos()):
                        self.restartGame()

            pygame.display.set_caption("Flappy Bird")
            self.updateveryThing(dt) 
            self.checkCollision()
            self.checkScore()
            self.draweveryThing()
            pygame.display.update() 
            self.clock.tick(60)

    def restartGame(self):
        self.score = 0
        self.score_text = self.font.render("0", True, (0,0,0))  # Re-render score text
        self.enter_pressed = False
        self.gameStarted = True
        self.bird.reset()
        self.pipes.clear()
        self.pipe_generator = 0
        self.bird.update_on = False
        self.startMonitoring = False  # Reset startMonitoring flag

    def setUpbgandg(self):
        self.bgimg=pygame.transform.scale_by(pygame.image.load('fpbg.jpg').convert(),self.scale_factor)
        self.ground1img = pygame.transform.scale_by(pygame.image.load('fpground.jpg').convert(), self.scale_factor)
        self.ground2img = pygame.transform.scale_by(pygame.image.load('fpground.jpg').convert(), self.scale_factor)

        self.ground1_rect = self.ground1img.get_rect()
        self.ground2_rect = self.ground2img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = self.ground2_rect.y = 450

    def updateveryThing(self, dt):
        if self.enter_pressed :
            #Moving the Groung
            self.ground1_rect.x -= int(self.velocity * dt)
            self.ground2_rect.x -= int(self.velocity * dt)

            if self.ground1_rect.right < 0 :
                self.ground1_rect.x = self.ground2_rect.right

            if self.ground2_rect.right < 0 :
                self.ground2_rect.x = self.ground1_rect.right

            #Generating Pipes
            if self.pipe_generator > 70: 
                self.pipes.append(Pipe(self.velocity))
                self.pipe_generator = 0

            self.pipe_generator += 1

            for pipe in self.pipes : #Moving the pipes
                pipe.update(dt)
            
            #Removing Pipes
            if len(self.pipes)!= 0:
                if self.pipes[0].rect_up.right < 0 :
                    self.pipes.pop(0) 
            
            self.bird.update(dt) #Moving the bird

    def checkScore(self):
        if len(self.pipes) > 0:
            pipe = self.pipes[0] 
            if (
                self.bird.rect.left > pipe.rect_down.left
                and self.bird.rect.right < pipe.rect_down.right
                and not self.startMonitoring
            ):
                self.startMonitoring = True

            if self.bird.rect.left > pipe.rect_down.right and self.startMonitoring:
                self.startMonitoring = False
                self.score += 1
                self.score_text = self.font.render(str(self.score), True, (0,0,0))  # Re-render score text

    def checkCollision(self):
        if len(self.pipes):
            if self.bird.rect.bottom > 447:
                self.bird.update_on = False
                self.enter_pressed = False
                self.gameStarted = False

            if(self.bird.rect.colliderect(self.pipes[0].rect_up) or self.bird.rect.colliderect(self.pipes[0].rect_down)) :
                self.enter_pressed = False
                self.gameStarted = False

    def draweveryThing(self):
        self.display.blit(self.bgimg, (0, 0))
        for pipe in self.pipes : 
            pipe.drawPipe(self.display)
        self.display.blit(self.ground1img, self.ground1_rect)
        self.display.blit(self.ground2img, self.ground2_rect)
        self.display.blit(self.bird.bird, self.bird.rect)
        self.display.blit(self.score_text, self.score_text_rect)
        if not self.gameStarted :
            self.display.blit(self.restart_text, self.restart_text_rect)

game = Game()