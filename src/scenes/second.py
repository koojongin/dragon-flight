import math
import sys

import pygame

from libs import ptext
from src.constant import MAPLE_STORY_BOLD_FONT
from src.interfaces.i_application import IApplication
from src.scenes.scene import GameScene


class SecondScene(GameScene):
    bg_y_position = 0
    is_playing = False

    def __init__(self, application: IApplication):
        self.application = application
        return

    def play(self):
        self.is_playing = True

        app = self.application
        screen = self.application.screen
        image = self.application.image
        audio = self.application.audio

        projectile_motion_index = 0
        selectable_characters = [
            image[f"character_illust_{str(value).zfill(2)}_lv1"]
            for value in range(1, 16)
        ]
        selected = selectable_characters[0]
        selected_character_index = 0

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
                        app.next_scene()

                    if event.key == pygame.K_LEFT:
                        if selected_character_index > 0:
                            selected_character_index -= 1

                        selected = selectable_characters[selected_character_index]

                    if event.key == pygame.K_RIGHT:
                        if selected_character_index < 14:
                            selected_character_index += 1

                        selected = selectable_characters[selected_character_index]

            bg = image["bg-stage2"]
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
            mid_line_first_y = top_text_display_y + 30

            selected = pygame.transform.scale(
                selected,
                (
                    screen.get_width() + 30,
                    app.get_height_by_width(screen.get_width() + 30, selected),
                ),
            )
            screen.blit(
                selected,
                (
                    screen.get_width() / 2 - selected.get_width() / 2,
                    screen.get_height() / 2
                    - selected.get_height() / 2
                    + math.sin(projectile_motion_index) * 5,
                ),
            )

            projectile_motion_index += 0.05

            ######
            pygame.display.update()
