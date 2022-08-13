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
        # self.bullets = []

        self.is_destroyed = False

    def set_speed(self, speed):
        self.speed = speed

    def set_max_hp(self, hp):
        self.max_hp = hp

    def set_current_hp(self, hp):
        self.current_hp = hp

    def fire(self, target_position):
        bullet = Bullet(self.arrow_image, app=self.app)
        bullet_x = self.position[0] + self.image.get_width() / 2 - bullet.image.get_width() / 2
        bullet_y = self.position[1] + self.image.get_height() / 2 - bullet.image.get_height() / 2
        bullet.position = (bullet_x, bullet_y)
        bullet.departure = bullet.position
        bullet.destination = target_position
        self.app.game_objects.append(bullet)

    def destroy(self, by_player_attack):
        self.app.audio["effect/monster_death.wav"].play()
        # self.bullets = []

        if by_player_attack:
            coin = Coin(self.app, check_colliders=self.check_colliders)
            coin.set_position(
                (self.position[0] + self.image.get_width() / 2, self.position[1] + self.image.get_height() / 2))
            coin.get_coin()
            self.app.game_objects.append(coin)

        self.is_destroyed = True

    def on_collision(self, target):
        target_class_name = type(target).__name__

        if target_class_name.find("Bullet") >= 0:
            self.current_hp -= target.damage
            print(target_class_name, self.current_hp)

        if self.current_hp <= 0:
            self.destroy(by_player_attack=True)

    def get_rect(self):
        return pygame.Rect(self.position, (self.image.get_width(), self.image.get_height()))

    def update(self):
        player = self.app.current_scene.player
        delta_time = self.app.delta_time
        screen = self.app.current_scene.screen

        if self.is_destroyed is True:
            self.app.game_objects.remove(self)
            return

        screen.blit(self.image, (self.position[0], self.position[1]))

        if self.bullet_cooldown_count <= 0:
            self.fire(
                (
                    player.position[0] + player.rect.width / 2,
                    player.position[1] + player.rect.height / 2,
                )
            )
            self.bullet_cooldown_count = self.bullet_cooldown
        self.position = (self.position[0], self.position[1] + self.speed * delta_time)
        if self.position[1] > screen.get_height():
            self.app.game_objects.remove(self)
            return

        self.bullet_cooldown_count -= delta_time

        # for bullet in self.bullets:
        #     screen.blit(bullet.image, (bullet.position[0], bullet.position[1]))
        #     bullet.update(self, delta_time)
        #     bullet.check_collision([player])
        #     if bullet.is_destroyed is True:
        #         self.bullets.remove(bullet)
