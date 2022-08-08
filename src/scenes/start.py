import math
import os
import sys

import pygame

from libs import ptext
from src.constant import MAPLE_STORY_BOLD_FONT
from src.scenes.scene import GameScene

PROJECT_PATH = os.path.abspath(os.curdir)
FONT_PATH = f"{PROJECT_PATH}/resources/font/Maplestory Bold.ttf"


class FirstScene(GameScene):
    bg_y_position = 0
    is_playing = False

    def __init__(self, application):
        self.application = application

    def play(self):
        self.is_playing = True
        app = self.application
        screen = self.application.screen
        image = self.application.image
        font = pygame.font.Font(FONT_PATH, 20)

        app.audio['bgm_acuarium'].set_volume(0.5)
        app.audio['bgm_acuarium'].play(-1)
        i = 0
        while self.is_playing:

            delta_time = app.clock.tick(app.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        app.audio['bgm_acuarium'].stop()
                        app.next_scene()

            #
            bg = image['bg-stage1']
            screen.blit(bg, [0, (0 - bg.get_height()) + self.bg_y_position])
            screen.blit(bg, [0, 0 + self.bg_y_position])
            screen.blit(bg, [0, (0 + bg.get_height()) + self.bg_y_position])
            if self.bg_y_position >= bg.get_height():
                self.bg_y_position = 0
            self.bg_y_position += 1

            #
            bg_character = image['character_illust_01_lv1']
            bg_character = pygame.transform.scale(bg_character, (
                screen.get_width() - 20, app.get_height_by_width(screen.get_width() - 20, bg_character)))

            bg_character_base_y_position = 100
            bg_character_y = bg_character_base_y_position + math.sin(i)*5
            screen.blit(bg_character, [10, bg_character_y])
            i += 0.05

            #
            logo = image['logo']

            scale_height = 170
            scaled_width = app.get_width_by_height(scale_height, logo)
            screen.blit(pygame.transform.scale(logo, (scaled_width, scale_height)),
                        (screen.get_width() / 2 - scaled_width / 2, 40))

            #
            # text_title = font.render("아무키나 누르세요", True, (255, 255, 255))
            text_title = ptext.draw("아무키나 누르세요", (-99, -99), owidth=1.1, ocolor=(255, 255, 255), color=(0, 0, 0),
                                    fontname=MAPLE_STORY_BOLD_FONT)
            text_position = (
                screen.get_width() / 2 - text_title[0].get_width() / 2,
                screen.get_height() - text_title[0].get_height() - 85)

            screen.blit(text_title[0], text_position)

            #
            pygame.display.update()
