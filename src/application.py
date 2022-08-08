import os
import sys

import pygame

from src.scenes.second import SecondScene
from src.scenes.start import FirstScene

PROJECT_PATH = os.path.abspath(os.curdir)
IMAGE_PATH = f"{PROJECT_PATH}/resources/images"
AUDIO_PATH = f"{PROJECT_PATH}/resources/audios"


class Application:
    image = {}
    audio = {}
    scenes = []
    current_scene = None
    fps = 60
    current_scene_index = None

    def __init__(self, title, screen_size):
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode(screen_size)
        self.load_images()
        self.load_scenes()
        self.set_scene(0)

    def run(self):
        while True:
            self.current_scene.play()

    def next_scene(self):
        self.set_scene(self.current_scene_index + 1)

    def load_scenes(self):
        self.scenes.append(FirstScene(self))
        self.scenes.append(SecondScene(self))

    def load_images(self):
        self.image['bg-stage1'] = pygame.image.load(IMAGE_PATH + "/background/01.png")
        self.image['bg-stage2'] = pygame.image.load(IMAGE_PATH + "/background/02.png")
        self.image['logo'] = pygame.image.load(IMAGE_PATH + "/logo.png")

    def load_audios(self):
        self.audio['bgm_waiting'] = pygame.image.load(IMAGE_PATH + "/background/02.png")

    def set_scene(self, index):
        self.current_scene_index = index
        self.current_scene = self.scenes[index]

    def get_width_by_height(self, height, image):
        origin_width = image.get_width()
        origin_height = image.get_height()
        return origin_width / origin_height * height

    def get_height_by_width(self, width, image):
        origin_width = image.get_width()
        origin_height = image.get_height()
        return origin_width / origin_height * width
