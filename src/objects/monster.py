import math

import pygame

from src.interfaces.i_application import IApplication


def calculate_distance_line(a, b):
    (x1, y1) = a
    (x2, y2) = b
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def calculate_distance_dot(a, b):
    dist = math.sqrt((a - b) ** 2)
    return dist


class Monster:
    x = 0
    y = 0
    speed = 0.1
    max_hp = 10
    current_hp = 10
    bullet_cooldown = 1000
    bullet_cooldown_count = bullet_cooldown

    bullets = []

    is_destroy = False

    def __init__(self, image, position=(0, 0), arrow_image=None):
        self.image = image
        if arrow_image is not None:
            self.arrow_image = arrow_image

        if position is not None:
            self.x = position[0]
            self.y = position[1]

    def fire(self, target_position):
        bullet = Bullet(self.arrow_image)
        bullet.x = self.x
        bullet.y = self.y
        bullet.departure = (bullet.x, bullet.y)
        bullet.destination = target_position
        self.bullets.append(bullet)

    def destroy(self):
        bullets = []
        self.is_destroy = True


class Bullet:
    x = 0
    y = 0
    speed = 0.1
    destination = (0, 0)
    departure = (0, 0)
    is_destroy = False

    def __init__(self, image, position=(0, 0)):
        self.image = image
        self.x = position[0]
        self.y = position[1]

    def destroy(self):
        self.is_destroy = True

    def update(self, scene, delta_time):
        is_close = False
        if (
                calculate_distance_dot(self.x, self.destination[0]) <= 5
                and calculate_distance_dot(self.y, self.destination[1]) <= 5
        ):
            is_close = True
            self.destroy()

        if is_close is False:
            print(self.speed, delta_time)
            self.x += (self.destination[0] - self.departure[0]) / (self.speed * delta_time * 30)
            self.y += (self.destination[1] - self.departure[1]) / (self.speed * delta_time * 30)


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

    def __init__(self, image, position=(0, 0)):
        super(Player, self).__init__()
        self.image = image
        self.sprites.append(image)
        self.x = position[0]
        self.y = position[1]
        self.rect = pygame.Rect((self.x, self.y), (self.image.get_size()))

    def set_application(self, app):
        self.app = app

    def update(self):

        self.index += 1
        self.rect = pygame.Rect((self.x, self.y), (self.rect.width, self.rect.height))
        if self.index >= len(self.sprites):
            self.index = 0

        self.image = self.sprites[self.index]

        move_delta = self.speed * self.delta_time

        if self.state == "left":
            result = self.x - move_delta
            if result <= 0:
                result = self.x
            self.x = result

        if self.state == "right":
            result = self.x + move_delta
            if result >= self.app.current_scene.screen.get_width() - self.rect.width:
                result = self.x
            self.x = result

    def destroy(self):
        self.is_destroy = True

    def move_left(self):
        self.state = "left"

    def move_right(self):
        self.state = "right"
