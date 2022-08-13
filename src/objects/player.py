import pygame

from src.interfaces.i_application import IApplication
from src.objects.bullets.PlayerBullet import PlayerBullet


class Player(pygame.sprite.Sprite):
    def __init__(
            self,
            image,
            app,
            position=(0, 0),
    ):
        super(Player, self).__init__()
        self.app: IApplication = app
        self.image = image
        self.position = position
        self.rect = pygame.Rect(self.position, (self.image.get_size()))

        ###
        self.max_hp = 3
        self.current_hp = self.max_hp
        self.missile_speed = 0.5
        self.missile_cooldown = 200
        self.missile_cooldown_count = 0

        self.speed = 0.3
        self.destination = (0, 0)
        self.is_destroyed = False
        self.state = "neutral"  # left,right,neutral
        self.index = 0
        self.alphas = []
        self.sprites = []
        self.keys = {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
        }

        self.setup_sprites(app.data["selected_character_index"])

    def setup_sprites(self, character_number=0):
        # self.sprites.append(self.image)
        character_number = str(character_number + 1).zfill(2)
        app = self.app
        sunny: pygame.Surface = app.image[
            f"character/sunny/sunny_{character_number}.png"
        ]
        sunny = sunny.subsurface((0, 5, 40, 115))
        scale_value = 0.5
        sunny = pygame.transform.scale(
            sunny, (sunny.get_width() * scale_value, sunny.get_height() * scale_value)
        )
        self.image = sunny
        self.sprites.append(sunny)

        self.rect = pygame.Rect(
            (self.position[0], self.position[1]), (self.image.get_width(), self.image.get_height())
        )

    def fire(self):
        character_number = self.app.data["selected_character_index"]
        character_number = str(character_number + 1).zfill(2)
        bullet = PlayerBullet(
            self.app.current_scene.image[
                f"character/weapon/bullet_{character_number}_01.png"
            ],
            speed=self.missile_speed,
            damage=int(character_number) + 1,
            app=self.app
        )
        if bullet.image.get_width() > 30:
            bullet.set_image_width(30)

        bullet_x = self.position[0] + (self.image.get_width() / 2) - bullet.image.get_width() / 2
        bullet_y = self.position[1] + self.image.get_height() / 2 - bullet.image.get_height() / 2
        bullet.position = (bullet_x, bullet_y)
        bullet.departure = self.position
        bullet.destination = (self.position[0], -100)
        self.app.game_objects.append(bullet)

    def update(self, *args):
        self.rect = pygame.Rect(
            (self.position[0], self.position[1]), (self.image.get_width(), self.image.get_height())
        )
        self.index += 1
        self.update_sprites()
        self.update_movement()
        self.update_missile_cooldown()
        self.deadline_auto_suicide()

    def deadline_auto_suicide(self):
        if self.position[1] <= -100:
            self.destroy()

    def update_missile_cooldown(self):
        if self.missile_cooldown_count <= 0:
            self.fire()
            self.missile_cooldown_count = self.missile_cooldown
        self.missile_cooldown_count -= self.delta_time

    def update_sprites(self):
        if self.index >= len(self.sprites):
            self.index = 0

        self.image = self.sprites[self.index]

        if self.alphas.__len__() > 0:
            self.image.set_alpha(self.alphas[0])
            self.alphas.pop(0)

    def update_movement(self):
        move_delta = self.speed * self.delta_time

        if self.keys["left"] is True:
            result = self.position[0] - move_delta
            if result <= 0:
                result = self.position[0]
            self.position = (result, self.position[1])

        if self.keys["right"] is True:
            result = self.position[0] + move_delta
            if result >= self.app.current_scene.screen.get_width() - self.rect.width:
                result = self.position[0]
            self.position = (result, self.position[1])

        if self.keys["up"] is True:
            result = self.position[1] - move_delta
            if result <= 0:
                result = self.position[1]
            self.position = (self.position[0], result)

        if self.keys["down"] is True:
            result = self.position[1] + move_delta
            if result >= self.app.current_scene.screen.get_height() - self.rect.height:
                result = self.position[1]
            self.position = (self.position[0], result)

    def destroy(self):
        self.is_destroyed = True
        print("DIE")

    def on_event_keydown(self, key):
        if key == pygame.K_LEFT:
            self.keys["left"] = True
        if key == pygame.K_RIGHT:
            self.keys["right"] = True
        if key == pygame.K_UP:
            self.keys["up"] = True
        if key == pygame.K_DOWN:
            self.keys["down"] = True

    def on_event_keyup(self, key):
        if key == pygame.K_LEFT:
            self.keys["left"] = False
        if key == pygame.K_RIGHT:
            self.keys["right"] = False
        if key == pygame.K_UP:
            self.keys["up"] = False
        if key == pygame.K_DOWN:
            self.keys["down"] = False

    def on_collision(self, target):
        target_class_name = type(target).__name__
        if target_class_name == "Bullet":
            self.current_hp -= 1
            self.alphas = [10, 10, 255, 10, 10, 255, 10, 10, 255, 10, 10, 255]
            if self.current_hp <= 0:
                self.destroy()

        if target_class_name.find("Monster") >= 0:
            self.current_hp = 0
            self.destroy()

    def get_rect(self):
        return pygame.Rect(self.position, (self.image.get_width(), self.image.get_height()))
