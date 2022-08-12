import pygame

from src.objects.coin import Coin
from src.objects.monster import Monster


class MonsterCandy(Monster):

    def __init__(self, image, position=(0, 0), arrow_image=None, app=None, check_colliders=[]):
        super().__init__(image, position, arrow_image, app, check_colliders)
        hp = 3
        self.set_speed(0.1)
        self.set_max_hp(hp)
        self.set_current_hp(hp)

    def get_rect(self):
        return super().get_rect()

    def fire(self, target_position):
        super().fire(target_position)

    def set_speed(self, speed):
        super().set_speed(speed)

    def set_max_hp(self, hp):
        super().set_max_hp(hp)

    def set_current_hp(self, hp):
        super().set_current_hp(hp)

    def destroy(self, by_player_attack):
        self.app.audio["effect/candy_death.mp3"].play()
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
        is_collision = pygame.Rect.colliderect(self.get_rect(), target.get_rect())
        if target_class_name == "Bullet" and is_collision:
            if is_collision:
                self.current_hp -= target.damage
                if self.current_hp <= 0:
                    self.destroy(by_player_attack=True)

        if target_class_name == "Player" and is_collision:
            if is_collision:
                # target.destroy()
                pass
