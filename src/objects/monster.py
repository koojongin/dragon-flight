import datetime
import math

from src.objects.bullet import Bullet


class Monster:
    def __init__(self, image, position=(0, 0), arrow_image=None):
        self.image = image
        if arrow_image is not None:
            self.arrow_image = arrow_image

        self.x = position[0]
        self.y = position[1]

        self.speed = 0.1
        self.max_hp = 10
        self.current_hp = 10
        self.bullet_cooldown = 1000
        self.bullet_cooldown_count = self.bullet_cooldown

        self.bullets = []

        self.is_destroy = False

    def fire(self, target_position):
        bullet = Bullet(self.arrow_image)
        bullet.x = self.x + self.image.get_width() / 2 - bullet.image.get_width() / 2
        bullet.y = self.y + self.image.get_height() / 2 - bullet.image.get_height() / 2
        bullet.departure = (bullet.x, bullet.y)
        bullet.destination = target_position
        self.bullets.append(bullet)

    def destroy(self):
        bullets = []
        self.is_destroy = True
