import pygame

from src.interfaces.i_application import IApplication
from src.objects.bullet import Bullet
from src.objects.util import calculate_distance_dot, get_height_by_width


class PlayerBullet(Bullet):
    def __init__(self, image, position=(0, 0), speed=0.2, damage=1, app: IApplication = None):
        super().__init__(image, position, speed, damage, app)

    def set_damage(self, damage):
        super().set_damage(damage)

    def set_image_width(self, width):
        super().set_image_width(width)

    def destroy(self):
        super().destroy()

    def update(self):
        screen = self.app.current_scene.screen
        delta_time = self.app.delta_time
        screen.blit(self.image, self.position)
        if (
                calculate_distance_dot(self.position[0], self.destination[0] + 800) <= 5
                and calculate_distance_dot(self.position[1], self.destination[1] + 800) <= 5
        ):
            self.destroy()
            return

        distance_x = calculate_distance_dot(self.destination[0], self.departure[0])
        distance_y = calculate_distance_dot(self.destination[1], self.departure[1])

        sdt = self.speed * delta_time
        direction_x = 1
        direction_y = 1
        if self.departure[0] > self.destination[0]:
            direction_x = -1

        if self.departure[1] > self.destination[1]:
            direction_y = -1

        if distance_y >= distance_x:
            position_x = self.position[0] + (sdt * direction_x * (distance_x / distance_y))
            position_y = self.position[1] + (sdt * direction_y)
            self.position = (position_x, position_y)

        if distance_y < distance_x:
            position_x = self.position[0] + (sdt * direction_x)
            position_y = self.position[1] + (sdt * direction_y * (distance_y / distance_x))
            self.position = (position_x, position_y)

        self.check_collision(self.app.game_objects)

    def check_collision(self, targets):
        bullet_rect = pygame.Rect(
            self.position[0], self.position[1], self.image.get_width(), self.image.get_height()
        )
        for target in targets:
            target_class_name = type(target).__name__
            if target_class_name.find('Monster') < 0:
                continue
            target_rect = pygame.Rect(
                target.position, (target.image.get_width(), target.image.get_height())
            )
            is_collision = pygame.Rect.colliderect(bullet_rect, target_rect)
            if is_collision:
                target.on_collision(self)
                self.destroy()

    def get_rect(self):
        return pygame.Rect(self.position, (self.image.get_width(), self.image.get_height()))
