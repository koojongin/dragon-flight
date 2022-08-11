import pygame

from src.interfaces.i_application import IApplication
from src.objects.bullet import Bullet


class Player(pygame.sprite.Sprite):
    x = 0
    y = 0
    speed = 0.3
    destination = (0, 0)
    is_destroy = False
    state = "neutral"  # left,right,neutral
    index = 0
    sprites = []
    delta_time = 0
    app: IApplication = None

    keys = {
        "right": False,
        "left": False,
        "up": False,
        "down": False,
    }

    def __init__(self, image, app, position=(0, 0), ):
        super(Player, self).__init__()
        self.app = app
        self.image = image
        self.sprites.append(image)
        self.x = position[0]
        self.y = position[1]
        self.rect = pygame.Rect((self.x, self.y), (self.image.get_size()))

        ###
        self.max_hp = 3
        self.current_hp = self.max_hp
        self.missiles = []
        self.missile_speed = 0.5
        self.missile_cooldown = 200
        self.missile_cooldown_count = self.missile_cooldown

    def fire(self):
        bullet = Bullet(self.app.current_scene.image["character/weapon/bullet_01_01.png"], speed=self.missile_speed)
        bullet.x = self.x + self.image.get_width() / 2 - bullet.image.get_width() / 2
        bullet.y = self.y + self.image.get_height() / 2 - bullet.image.get_height() / 2
        bullet.departure = (self.x, self.y)
        bullet.destination = (self.x, -100)
        self.missiles.append(bullet)

    def update(self, *args):
        self.index += 1
        self.rect = pygame.Rect((self.x, self.y), (self.rect.width, self.rect.height))
        if self.index >= len(self.sprites):
            self.index = 0

        self.image = self.sprites[self.index]

        move_delta = self.speed * self.delta_time

        if self.keys["left"] is True:
            result = self.x - move_delta
            if result <= 0:
                result = self.x
            self.x = result

        if self.keys["right"] is True:
            result = self.x + move_delta
            if result >= self.app.current_scene.screen.get_width() - self.rect.width:
                result = self.x
            self.x = result

        if self.keys["up"] is True:
            result = self.y - move_delta
            if result <= 0:
                result = self.y
            self.y = result

        if self.keys["down"] is True:
            result = self.y + move_delta
            if result >= self.app.current_scene.screen.get_height() - self.rect.height:
                result = self.y
            self.y = result

    def destroy(self):
        self.is_destroy = True

    def on_event_keydown(self, key):
        if key == pygame.K_LEFT:
            self.keys["left"] = True
        if key == pygame.K_RIGHT:
            self.keys["right"] = True
        if key == pygame.K_UP:
            self.keys["up"] = True
        if key == pygame.K_DOWN:
            self.keys["down"] = True

    def on_event_keyup(self, key):
        if key == pygame.K_LEFT:
            self.keys["left"] = False
        if key == pygame.K_RIGHT:
            self.keys["right"] = False
        if key == pygame.K_UP:
            self.keys["up"] = False
        if key == pygame.K_DOWN:
            self.keys["down"] = False

    def on_collision(self, target):
        print("?", self.current_hp, target)
        self.current_hp -= 1

        if self.current_hp <= 0:
            self.destroy()
