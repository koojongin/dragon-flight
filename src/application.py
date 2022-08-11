import asyncio
import os
import sys

import pygame

from src.constant import PROJECT_PATH, FPS
from src.interfaces.i_application import IApplication
from src.scenes.character_selection import SecondScene
from src.scenes.stage import StageScene
from src.scenes.start import FirstScene

IMAGE_PATH = f"{PROJECT_PATH}/resources/images"
AUDIO_PATH = f"{PROJECT_PATH}/resources/audios"


class Application(IApplication):
    image = {}
    audio = {}
    scenes = []
    current_scene = None
    fps = FPS
    current_scene_index = None
    data = {}

    def __init__(self, title, screen_size):
        # pygame.mixer.pre_init(44100, 16, 2, 4096)
        self.clock = pygame.time.Clock()
        pygame.init()
        self.image["favicon"] = pygame.image.load(f"{IMAGE_PATH}/icon.png")
        scaled_favicon = pygame.transform.scale(self.image["favicon"], (32, 32))
        pygame.display.set_icon(scaled_favicon)
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode(screen_size)
        self.load_images()
        self.load_audios()
        self.load_scenes()
        self.set_scene(0)

    def run(self):
        self.after_resources_load()
        self.current_scene.play()

    def after_resources_load(self):
        print("on_load")
        for character_number in range(1, 16):
            for character_level in range(1, 4):
                lv_string = ""
                if character_level != 1:
                    lv_string = f"_lv{character_level}"
                self.image[
                    f"sd_{str(character_number).zfill(2)}{lv_string}"
                ] = pygame.image.load(
                    IMAGE_PATH
                    + f"/character/sd/sd_{str(character_number).zfill(2)}{lv_string}.png"
                )

        self.image["bg-stage2"] = pygame.image.load(IMAGE_PATH + "/background/02.png")
        self.image["bg-stage3"] = pygame.image.load(IMAGE_PATH + "/background/03.png")
        self.image["bg-stage4"] = pygame.image.load(IMAGE_PATH + "/background/04.png")
        self.image["bg-stage5"] = pygame.image.load(IMAGE_PATH + "/background/05.png")
        self.image["bg-stage6"] = pygame.image.load(IMAGE_PATH + "/background/25.png")

        for (dirpath, dirnames, filenames) in os.walk(f"{IMAGE_PATH}/monsters"):
            for filename in filenames:
                self.image[f"monsters/{filename}"] = pygame.image.load(
                    f"{dirpath}/{filename}"
                )

        for (dirpath, dirnames, filenames) in os.walk(f"{IMAGE_PATH}/character/sunny"):
            for filename in filenames:
                self.image[f"character/sunny/{filename}"] = pygame.image.load(
                    f"{dirpath}/{filename}"
                )

        for (dirpath, dirnames, filenames) in os.walk(f"{IMAGE_PATH}/character/weapon"):
            for filename in filenames:
                self.image[f"character/weapon/{filename}"] = pygame.image.load(
                    f"{dirpath}/{filename}"
                )

        for (dirpath, dirnames, filenames) in os.walk(f"{IMAGE_PATH}/ui"):
            for filename in filenames:
                self.image[f"ui/{filename}"] = pygame.image.load(
                    f"{dirpath}/{filename}"
                )
        print("on_load_complete")

    def select_scene(self, index):
        self.set_scene(index)
        self.current_scene.play()

    def next_scene(self):
        self.current_scene.is_playing = False
        self.set_scene(self.current_scene_index + 1)
        self.current_scene.play()

    def load_scenes(self):
        # Scene 순서대로
        self.scenes.append(FirstScene(self))
        self.scenes.append(SecondScene(self))
        self.scenes.append(StageScene(self))

    def load_images(self):
        self.image["ui/grac.png"] = pygame.image.load(IMAGE_PATH + "/ui/grac.png")
        self.image["illust/first_login.png"] = pygame.image.load(
            IMAGE_PATH + "/illust/first_login.png"
        )
        self.image["bg-stage1"] = pygame.image.load(IMAGE_PATH + "/background/01.png")
        for character_number in range(1, 16):
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
