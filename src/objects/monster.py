import datetime
import math

import pygame

from src.interfaces.i_application import IApplication
from src.objects.bullet import Bullet
from src.objects.coin import Coin


class Monster:
    def __init__(self, image, position=(0, 0), arrow_image=None, app=None, check_colliders=[]):
        self.image = image
        self.app: IApplication = app
        if arrow_image is not None:
            self.arrow_image = arrow_image

        self.position = position

        self.speed = 0.1
        self.max_hp = 5
        self.current_hp = 5
        self.bullet_cooldown = 1000
        self.bullet_cooldown_count = self.bullet_cooldown
        self.check_colliders = check_colliders
        self.bullets = []

        self.is_destroy = False

    def set_speed(self, speed):
        self.speed = speed

    def set_max_hp(self, hp):
        self.max_hp = hp

    def set_current_hp(self, hp):
        self.current_hp = hp

    def fire(self, target_position):
        bullet = Bullet(self.arrow_image)
        bullet_x = self.position[0] + self.image.get_width() / 2 - bullet.image.get_width() / 2
        bullet_y = self.position[1] + self.image.get_height() / 2 - bullet.image.get_height() / 2
        bullet.position = (bullet_x, bullet_y)
        bullet.departure = bullet.position
        bullet.destination = target_position
        self.bullets.append(bullet)

    def destroy(self, by_player_attack):
        self.app.audio["effect/monster_death.wav"].play()
        self.bullets = []

        if by_player_attack:
            score = self.app.current_scene.data.get('score')
            if score is not None:
                self.app.current_scene.data['score'] += 1
            coin = Coin(self.app, check_colliders=self.check_colliders)
            coin.set_position(
                (self.position[0] + self.image.get_width() / 2, self.position[1] + self.image.get_height() / 2))
            self.app.game_objects.append(coin)

        self.is_destroy = True

    def on_collision(self, target):
        target_class_name = type(target).__name__

        if target_class_name == "Bullet":
            self.current_hp -= target.damage

        if self.current_hp <= 0:
            self.destroy(by_player_attack=True)

    def get_rect(self):
        return pygame.Rect(self.position, (self.image.get_width(), self.image.get_height()))
