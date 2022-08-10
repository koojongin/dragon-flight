import pygame

from src.interfaces.i_application import IApplication


class Player(pygame.sprite.Sprite):
    x = 0
    y = 0
    speed = 0.3
    destination = (0, 0)
    is_destroy = False
    state = "neutral"  # left,right,neutral
    index = 0
    sprites = []
    delta_time = 0
    app: IApplication = None

    keys = {
        "right": False,
        "left": False,
        "up": False,
        "down": False,
    }

    def __init__(self, image, position=(0, 0)):
        super(Player, self).__init__()
        self.image = image
        self.sprites.append(image)
        self.x = position[0]
        self.y = position[1]
        self.rect = pygame.Rect((self.x, self.y), (self.image.get_size()))

    def set_application(self, app):
        self.app = app

    def update(self):

        self.index += 1
        self.rect = pygame.Rect((self.x, self.y), (self.rect.width, self.rect.height))
        if self.index >= len(self.sprites):
            self.index = 0

        self.image = self.sprites[self.index]

        move_delta = self.speed * self.delta_time

        if self.keys["left"] is True:
            result = self.x - move_delta
            if result <= 0:
                result = self.x
            self.x = result

        if self.keys["right"] is True:
            result = self.x + move_delta
            if result >= self.app.current_scene.screen.get_width() - self.rect.width:
                result = self.x
            self.x = result

        if self.keys["up"] is True:
            result = self.y - move_delta
            if result <= 0:
                result = self.y
            self.y = result

        if self.keys["down"] is True:
            result = self.y + move_delta
            if result >= self.app.current_scene.screen.get_height() - self.rect.height:
                result = self.y
            self.y = result

    def destroy(self):
        self.is_destroy = True

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
