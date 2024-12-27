import pygame

class Bird(pygame.sprite.Sprite) :
    def __init__(self):
        super(Bird, self).__init__()
        self.bird_list = [pygame.image.load('birdup.png').convert_alpha(), 
                          pygame.image.load('birddown.png').convert_alpha()]
        self.bird_index = 0
        self.bird = self.bird_list[self.bird_index]
        self.rect = self.bird.get_rect(center=(125, 250))
        self.y_velocity = 0
        self.gravity = 10
        self.flapspeed = 250
        self.ani_counter = 0
        self.update_on = False

    def update(self,dt):
        self.playAnimation()
        self.applyGravity(dt)

        if self.rect.y <= 0 and self.flapspeed == 250:
            self.rect.y = 0
            self.flapspeed = 0
            self.y_velocity = 0
        
        elif self.rect.y > 0 and self.flapspeed == 0:
            self.flapspeed = 250

    def applyGravity(self, dt):
        if self.update_on:
            self.y_velocity += self.gravity * dt
            self.rect.y += self.y_velocity

    def flap(self, dt):
        self.y_velocity = - self.flapspeed * dt

    def playAnimation(self):
        if self.ani_counter == 5:
            self.bird = self.bird_list[self.bird_index]
            if self.bird_index == 0:
                self.bird_index = 1
            else :
                self.bird_index = 0
            self.ani_counter = 0 
          
        self.ani_counter += 1
        
    def reset(self):
        self.rect.center = (125, 250)
        self.ani_counter = 0
        self.y_velocity = 0