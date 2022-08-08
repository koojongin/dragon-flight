import sys
import time

import pygame

from libs import ptext
from src.constant import MAPLE_STORY_BOLD_FONT
from src.scenes.scene import GameScene


class SecondScene(GameScene):
    bg_y_position = 0

    def __init__(self, application):
        self.application = application
        return

    def play(self):
        app = self.application
        screen = self.application.screen
        image = self.application.image
        audio = self.application.audio

        audio['bgm_fortress_sky'].set_volume(0.7)
        audio['bgm_fortress_sky'].play(-1)

        while True:

            delta_time = app.clock.tick(app.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            bg = image['bg-stage2']
            screen.blit(bg, [0, (0 - bg.get_height()) + self.bg_y_position])
            screen.blit(bg, [0, 0 + self.bg_y_position])
            screen.blit(bg, [0, (0 + bg.get_height()) + self.bg_y_position])
            if self.bg_y_position >= bg.get_height():
                self.bg_y_position = 0
            self.bg_y_position += 1

            #
            text_title = ptext.draw("------- 캐릭터 선택 -------", (-99, -99), owidth=1.1, ocolor=(255, 255, 255),
                                    color=(0, 0, 0),
                                    fontname=MAPLE_STORY_BOLD_FONT)
            text_position = (
                screen.get_width() / 2 - text_title[0].get_width() / 2,
                25)

            screen.blit(text_title[0], text_position)

            #
            pygame.display.update()
