import datetime
import math

from src.interfaces.i_application import IApplication
from src.objects.bullet import Bullet
from src.objects.coin import Coin


class Monster:
    def __init__(self, image, position=(0, 0), arrow_image=None, app=None, check_colliders=[]):
        self.image = image
        self.app: IApplication = app
        if arrow_image is not None:
            self.arrow_image = arrow_image

        self.x = position[0]
        self.y = position[1]

        self.speed = 0.1
        self.max_hp = 5
        self.current_hp = 5
        self.bullet_cooldown = 1000
        self.bullet_cooldown_count = self.bullet_cooldown
        self.check_colliders = check_colliders
        self.bullets = []

        self.is_destroy = False

    def fire(self, target_position):
        bullet = Bullet(self.arrow_image)
        bullet.x = self.x + self.image.get_width() / 2 - bullet.image.get_width() / 2
        bullet.y = self.y + self.image.get_height() / 2 - bullet.image.get_height() / 2
        bullet.departure = (bullet.x, bullet.y)
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
            coin.set_position((self.x + self.image.get_width() / 2, self.y + self.image.get_height() / 2))
            self.app.game_objects.append(coin)

        self.is_destroy = True

    def on_collision(self, target):
        target_class_name = type(target).__name__

        if target_class_name == "Bullet":
            self.current_hp -= target.damage

        if self.current_hp <= 0:
            self.destroy(by_player_attack=True)
