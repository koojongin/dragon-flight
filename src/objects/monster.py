import datetime
import math

from src.objects.bullet import Bullet


class Monster:
    x = 0
    y = 0
    speed = 0.1
    max_hp = 10
    current_hp = 10
    bullet_cooldown = 100
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
