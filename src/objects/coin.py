import pygame
from pygame.surface import Surface

from src.interfaces.i_application import IApplication


class Coin:
    falling_speed = 0.5
    coin_value = 1

    def __init__(self, app: IApplication, position=(0, 0), check_colliders=[]):
        self.app = app
        self.screen = app.screen
        self.image = app.image['ui/coin.png']
        scale_value = 0.7
        self.image = pygame.transform.scale(self.image, (
            self.image.get_width() * scale_value, self.image.get_height() * scale_value))

        # initialize
        self.is_destroyed = False
        self.gold = 1
        self.position = position
        self.check_colliders = check_colliders

    def set_position(self, position):
        self.position = position

    def destroy(self):
        self.is_destroyed = True

    def update(self):
        self.screen.blit(self.image, self.position)
        self.position = (self.position[0], self.position[1] + self.falling_speed * self.app.delta_time)
        self.check_collision(self.check_colliders)

    def get_coin(self):
        score = self.app.current_scene.data.get('score')
        if score is not None:
            self.app.current_scene.data['score'] += self.coin_value
        self.app.audio['effect/gold_drop.wav'].play()

    def check_collision(self, targets):
        for target in targets:
            target_class_name = type(target).__name__
            if target_class_name == 'Player':
                coin_rect = pygame.Rect(self.position, (self.image.get_width(),
                                                        self.image.get_height()))
                is_collision = pygame.Rect.colliderect(coin_rect, target.rect)
                if is_collision:
                    self.app.audio['effect/gold_earn.mp3'].play()
                    self.app.current_scene.data['gold'] += 1
                    self.destroy()
