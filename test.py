from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width,height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOW] and self.rect.y < win_height-80:
            self.rect.y += self.speed

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height-80:
            self.rect.y += self.speed

#Game window
win_width = 600
win_height = 500

window = display.set_mode((win_width, win_height))
window.fill((50,70,123))

#Game state
game = True
finish = False

while game == True:
    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()