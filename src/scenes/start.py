import sys

import pygame

from src.scenes.scene import GameScene


class FirstScene(GameScene):
    clock = pygame.time.Clock()
    bg_y_position = 0

    def __init__(self, application):
        self.application = application
        return

    def play(self):
        delta_time = self.clock.tick(self.application.fps)
        app = self.application
        screen = self.application.screen
        image = self.application.image

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
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
        logo = image['logo']

        scale_height = 170
        scaled_width = app.get_height_by_width(scale_height, logo)
        screen.blit(pygame.transform.scale(logo, (scaled_width, scale_height)),
                    (screen.get_width() / 2 - scaled_width / 2, 40))

        #
        pygame.display.update()
