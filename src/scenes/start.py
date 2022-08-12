import math
import sys

import pygame

from libs import ptext
from src.constant import MAPLE_STORY_BOLD_FONT, FONT_PATH
from src.interfaces.i_application import IApplication
from src.objects.util import get_width_by_height, get_height_by_width
from src.scenes.scene import GameScene


class FirstScene(GameScene):
    bg_y_position = 0
    is_playing = False

    def __init__(self, application: IApplication):
        self.application = application

    def play(self):
        self.is_playing = True
        app = self.application
        screen = self.application.screen
        image = self.application.image
        font = pygame.font.Font(FONT_PATH, 20)

        app.audio["bgm_acuarium"].set_volume(0.5)
        app.audio["bgm_acuarium"].play(-1)

        bg = image["illust/first_login.png"]
        bg = pygame.transform.scale(
            bg,
            (
                screen.get_width() + 40,
                get_height_by_width(screen.get_width() + 40, bg),
            ),
        )

        i = 0
        while self.is_playing:

            delta_time = app.clock.tick(app.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        app.audio["bgm_acuarium"].stop()
                        app.audio["effect_select"].play()
                        app.next_scene()

            #
            screen.blit(
                bg,
                [
                    screen.get_width() / 2 - bg.get_width() / 2,
                    screen.get_height() / 2 - bg.get_height() / 2 + 25,
                ],
            )

            #
            grac = app.image["ui/grac.png"]
            screen.blit(
                grac,
                (
                    screen.get_width() - grac.get_width() - 10,
                    screen.get_height() - grac.get_height() - 10,
                ),
            )

            #
            # bg_character = image["character_illust_01_lv1"]
            # bg_character = pygame.transform.scale(
            #     bg_character,
            #     (
            #         screen.get_width() - 20,
            #         app.get_height_by_width(screen.get_width() - 20, bg_character),
            #     ),
            # )
            #
            # bg_character_base_y_position = 100
            # bg_character_y = bg_character_base_y_position + math.sin(i) * 5
            # screen.blit(bg_character, [10, bg_character_y])
            i += 0.05

            #
            logo = image["logo"]

            scale_height = 170
            scaled_width = get_width_by_height(scale_height, logo)
            screen.blit(
                pygame.transform.scale(logo, (scaled_width, scale_height)),
                (screen.get_width() / 2 - scaled_width / 2, 40),
            )

            #
            # text_title = font.render("아무키나 누르세요", True, (255, 255, 255))
            text_title = ptext.draw(
                '"스페이스 바"를 눌러 시작',
                (-99, -99),
                owidth=1.1,
                ocolor=(255, 255, 255),
                color=(0, 0, 0),
                fontname=MAPLE_STORY_BOLD_FONT,
                alpha=(math.sin(i) + 1.2),
            )
            text_position = (
                screen.get_width() / 2 - text_title[0].get_width() / 2,
                screen.get_height() - text_title[0].get_height() - 85,
            )

            screen.blit(text_title[0], text_position)

            #
            pygame.display.update()
