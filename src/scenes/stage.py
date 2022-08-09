import math
import sys

import pygame

from libs import ptext
from src.constant import MAPLE_STORY_BOLD_FONT
from src.interfaces.i_application import IApplication
from src.scenes.scene import GameScene


class StageScene(GameScene):
    bg_y_position = 0

    def __init__(self, application: IApplication):
        self.application = application
        return

    def play(self):
        app = self.application
        screen = self.application.screen
        image = self.application.image
        audio = self.application.audio

        audio["bgm_fortress_sky"].set_volume(0.5)
        audio["bgm_fortress_sky"].play(-1)

        while True:

            delta_time = app.clock.tick(app.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            bg = image["bg-stage3"]
            screen.blit(bg, [0, (0 - bg.get_height()) + self.bg_y_position])
            screen.blit(bg, [0, 0 + self.bg_y_position])
            screen.blit(bg, [0, (0 + bg.get_height()) + self.bg_y_position])
            if self.bg_y_position >= bg.get_height():
                self.bg_y_position = 0
            self.bg_y_position += 1

            # display - top text
            text_title = ptext.draw(
                "캐릭터 선택",
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
            character_select_area_padding = 20
            character_select_area_width = (
                screen.get_width()
                - character_select_area_padding * 2
                - (mid_horizontal_padding * 2)
            ) / 3

            mid_line_first_y = top_text_display_y + 30
            selectable_characters = [
                image[f"character_select_{str(value).zfill(2)}_lv1"]
                for value in range(1, 16)
            ]

            for index, selectable_character in enumerate(selectable_characters):
                floor = math.floor(index / 3)

                selectable_character = pygame.transform.scale(
                    selectable_character,
                    (character_select_area_width, character_select_area_width),
                )
                screen.blit(
                    selectable_character,
                    [
                        mid_horizontal_padding
                        + selectable_character.get_width() * (index % 3)
                        + character_select_area_padding * (index % 3),
                        mid_line_first_y
                        + floor * selectable_character.get_height()
                        + floor * character_select_area_padding,
                    ],
                )
            #
            pygame.display.update()
