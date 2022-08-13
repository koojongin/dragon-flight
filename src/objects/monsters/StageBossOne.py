import pygame

from src.objects.Bullet import Bullet
from src.objects.monster import Monster


class StageBossOneMonster(Monster):

    def __init__(self, app, position=(0, 0), check_colliders=[]):
        self.app = app
        self.image = self.app.image['monsters/baldhair.png']
        self.image = pygame.transform.scale2x(self.image)
        super().__init__(self.image, position, app=app)

        self.speed = 0.5
        self.bullet_cooldown = 3000
        self.bullet_cooldown_count = self.bullet_cooldown
        self.last_fired_at = 0
        self.fire_count = 0
        self.max_hp = 1000
        self.current_hp = self.max_hp

        self.action_state = 'to_right'

    def set_speed(self, speed):
        super().set_speed(speed)

    def set_max_hp(self, hp):
        super().set_max_hp(hp)

    def set_current_hp(self, hp):
        super().set_current_hp(hp)

    def fire(self, target_position):
        bullet_speed = 0.7
        bullet = Bullet(self.app.image['monsters/baldhair_arrow.png'], app=self.app, speed=bullet_speed)
        bullet_x = self.position[0] + self.image.get_width() / 2 - bullet.image.get_width() / 2
        bullet_y = self.position[1] + self.image.get_height() / 2 - bullet.image.get_height() / 2
        bullet.__name__ = 'gg'
        bullet.position = (bullet_x, bullet_y)
        bullet.departure = bullet.position
        bullet.destination = target_position
        self.app.game_objects.append(bullet)

    def fire_big_arrow(self, target_position):
        bullet_speed = 0.1
        image = self.app.image['monsters/baldhair_arrow.png']
        scale_value = 4
        image = pygame.transform.scale(image, (image.get_width() * scale_value, image.get_height() * scale_value))
        bullet = Bullet(image, app=self.app, speed=bullet_speed)
        bullet_x = self.position[0] + self.image.get_width() / 2 - bullet.image.get_width() / 2
        bullet_y = self.position[1] + self.image.get_height() / 2 - bullet.image.get_height() / 2
        bullet.position = (bullet_x, bullet_y)
        bullet.departure = bullet.position
        bullet.destination = target_position
        self.app.game_objects.append(bullet)

    def destroy(self, by_player_attack):
        super().destroy(by_player_attack)

    def on_collision(self, target):
        super().on_collision(target)

    def get_rect(self):
        return super().get_rect()

    def update(self):
        screen = self.app.current_scene.screen
        screen.blit(self.image, self.position)

        self.bullet_cooldown_count -= self.app.delta_time
        now = pygame.time.get_ticks()

        if self.bullet_cooldown_count <= 0:
            self.fire_count = 5
            self.last_fired_at = now
            self.bullet_cooldown_count = self.bullet_cooldown
            self.last_fired_position = self.app.current_scene.player.position

        if now - self.last_fired_at > 30 and self.fire_count > 0:
            self.last_fired_at = now
            self.fire_count -= 1
            self.fire(self.last_fired_position)
            if self.fire_count == 0:
                self.fire_big_arrow((self.position[0], screen.get_height()))

        self.run_actions(screen)

    def run_actions(self, screen):
        if self.action_state == "to_right":
            self.action_one(screen)
        if self.action_state == "to_left":
            self.action_two(screen)

    def action_one(self, screen):
        next_x_position = self.position[0] + self.speed * self.app.delta_time
        if next_x_position + self.image.get_width() > screen.get_width():
            next_x_position = screen.get_width() - self.image.get_width()
            self.action_state = "to_left"
        self.position = (next_x_position, 0)

    def action_two(self, screen):
        next_x_position = self.position[0] - self.speed * self.app.delta_time
        if next_x_position <= 0:
            next_x_position = 0
            self.action_state = "to_right"
        self.position = (next_x_position, 0)
