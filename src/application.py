import os
import sys

import pygame

from src.interfaces.i_application import IApplication
from src.scenes.second import SecondScene
from src.scenes.start import FirstScene

PROJECT_PATH = os.path.abspath(os.curdir)
IMAGE_PATH = f"{PROJECT_PATH}/resources/images"
AUDIO_PATH = f"{PROJECT_PATH}/resources/audios"


class Application(IApplication):
    image = {}
    audio = {}
    scenes = []
    current_scene = None
    fps = 60
    current_scene_index = None

    def __init__(self, title, screen_size):
        # pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        # pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode(screen_size)
        self.load_images()
        self.load_audios()
        self.load_scenes()
        self.set_scene(0)

    def run(self):
        self.clock = pygame.time.Clock()
        self.current_scene.play()

    def next_scene(self):
        self.current_scene.is_playing = False
        self.set_scene(self.current_scene_index + 1)
        self.current_scene.play()

    def load_scenes(self):
        self.scenes.append(FirstScene(self))
        self.scenes.append(SecondScene(self))

    def load_images(self):
        self.image["bg-stage1"] = pygame.image.load(IMAGE_PATH + "/background/01.png")
        self.image["bg-stage2"] = pygame.image.load(IMAGE_PATH + "/background/02.png")
        for character_number in range(1, 16):
            self.image[
                f"sunny_{str(character_number).zfill(2)}_lv1"
            ] = pygame.image.load(
                IMAGE_PATH
                + f"/character/sunny/sunny_{str(character_number).zfill(2)}.png"
            )
            for character_level in range(1, 4):
                lv_string = ""
                if character_level != 1:
                    lv_string = f"_lv{character_level}"
                self.image[
                    f"character_illust_{str(character_number).zfill(2)}_lv{character_level}"
                ] = pygame.image.load(
                    IMAGE_PATH
                    + f"/character/illust/character_{str(character_number).zfill(2)}{lv_string}.png"
                )
                self.image[
                    f"character_select_{str(character_number).zfill(2)}_lv{character_level}"
                ] = pygame.image.load(
                    IMAGE_PATH
                    + f"/character/select/select_character_{str(character_number).zfill(2)}{lv_string}.png"
                )
        self.image["bg-stage2"] = pygame.image.load(IMAGE_PATH + "/background/02.png")
        self.image["logo"] = pygame.image.load(IMAGE_PATH + "/logo.png")

    def load_audios(self):
        self.audio["bgm_waiting"] = pygame.mixer.Sound(
            "resources/audios/bgm_waiting.mp3"
        )
        self.audio["bgm_acuarium"] = pygame.mixer.Sound(
            "resources/audios/bgm_acuarium.mp3"
        )
        self.audio["bgm_fortress_sky"] = pygame.mixer.Sound(
            "resources/audios/bgm_fortress_sky.mp3"
        )

        self.audio["effect_select"] = pygame.mixer.Sound(
            "resources/audios/effect/select.mp3"
        )

    def set_scene(self, index):
        self.current_scene_index = index
        self.current_scene = self.scenes[index]

    def get_width_by_height(self, height, image):
        origin_width = image.get_width()
        origin_height = image.get_height()
        return (origin_width / origin_height) * height

    def get_height_by_width(self, width, image):
        origin_width = image.get_width()
        origin_height = image.get_height()
        return (origin_height / origin_width) * width
