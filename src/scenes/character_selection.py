import math
import sys

import pygame

from libs import ptext
from src.constant import MAPLE_STORY_BOLD_FONT
from src.interfaces.i_application import IApplication
from src.objects.sunny import get_sunny_name, Sunny
from src.scenes.scene import GameScene


class SecondScene(GameScene):
    bg_y_position = 0
    is_playing = False

    def __init__(self, application: IApplication):
        self.application = application
        app = self.application

        self.selectable_characters = [
            app.image[f"character_illust_{str(value).zfill(2)}_lv1"]
            for value in range(1, 16)
        ]
        self.selected_character_index = (
            app.data["selected_character_index"]
            if app.data.get("selected_character_index") is not None
            else 0
        )
        self.update_selected_sunny()

    def update_selected_sunny(self):
        self.selected_sunny = self.selectable_characters[self.selected_character_index]
        self.sunny = Sunny(get_sunny_name(self.selected_character_index))

    def play(self):
        self.is_playing = True

        app = self.application
        screen = self.application.screen
        image = self.application.image
        audio = self.application.audio

        projectile_motion_index = 0

        self.selected_sunny = self.selectable_characters[self.selected_character_index]

        audio["bgm_fortress_sky"].set_volume(0.5)
        audio["bgm_fortress_sky"].play(-1)

        while self.is_playing:

            delta_time = app.clock.tick(app.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        app.audio["bgm_fortress_sky"].stop()
                        app.audio["effect_select"].play()
                        self.is_playing = False
                        app.data[
                            "selected_character_index"
                        ] = self.selected_character_index
                        app.next_scene()

                    if event.key == pygame.K_LEFT:
                        if self.selected_character_index > 0:
                            self.selected_character_index -= 1

                        self.update_selected_sunny()

                    if event.key == pygame.K_RIGHT:
                        if self.selected_character_index < 14:
                            self.selected_character_index += 1

                        self.update_selected_sunny()

            bg = image["bg-stage2"]
            screen.blit(bg, [0, (0 - bg.get_height()) + self.bg_y_position])
            screen.blit(bg, [0, 0 + self.bg_y_position])
            screen.blit(bg, [0, (0 + bg.get_height()) + self.bg_y_position])
            if self.bg_y_position >= bg.get_height():
                self.bg_y_position = 0
            self.bg_y_position += 1

            # display - top text
            text_title = ptext.draw(
                self.sunny.name,
                (-99, -99),
                owidth=1.1,
                ocolor=(255, 255, 255),
                color=(0, 0, 0),
                fontname=MAPLE_STORY_BOLD_FONT,
            )
            text_position = (screen.get_width() / 2 - text_title[0].get_width() / 2, 25)

            screen.blit(text_title[0], text_position)

            # display - mid
            top_text_display_y = text_position[1] + text_title[0].get_height()
            mid_horizontal_padding = 30
            mid_line_first_y = top_text_display_y + 30

            self.selected_sunny = pygame.transform.scale(
                self.selected_sunny,
                (
                    screen.get_width() + 30,
                    app.get_height_by_width(screen.get_width() + 30, self.selected_sunny),
                ),
            )
            screen.blit(
                self.selected_sunny,
                (
                    screen.get_width() / 2 - self.selected_sunny.get_width() / 2,
                    screen.get_height() / 2
                    - self.selected_sunny.get_height() / 2
                    + math.sin(projectile_motion_index) * 5,
                ),
            )

            projectile_motion_index += 0.05

            ######
            pygame.display.update()
