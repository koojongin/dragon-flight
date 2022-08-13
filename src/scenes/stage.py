import sys
from copy import copy
from random import randrange

import pygame

from libs import ptext
from src.constant import MAPLE_STORY_BOLD_FONT
from src.interfaces.i_application import IApplication
from src.objects.monsters.Candy import MonsterCandy
from src.objects.monsters.StageBossOne import StageBossOneMonster
from src.objects.player import Player
from src.scenes.scene import GameScene
from src.scenes.start import FONT_PATH


class StageScene(GameScene):
    is_playing = False
    bg_y_position = 0
    elapsed_frame = 0

    def __init__(self, application: IApplication):
        self.application = application
        self.app = self.application
        self.screen = self.application.screen
        self.image = self.application.image
        self.audio = self.application.audio

        self.data = {
            "score": 0,
            "gold": 0
        }
        self.player = None
        self.app.game_objects = []

    def play(self):
        self.app.game_objects = []
        self.is_playing = True
        self.audio["bgm_till_the_end_of_infinity.mp3"].set_volume(0.5)
        self.audio["bgm_till_the_end_of_infinity.mp3"].play(-1)

        font = pygame.font.Font(FONT_PATH, 12)

        # values
        bg_y = 0

        monster_create_event = pygame.USEREVENT + 1
        pygame.time.set_timer(monster_create_event, 941)
        all_sprites = pygame.sprite.Group()
        player = Player(
            self.image["monsters/candy.png"],
            app=self.app,
            position=(0, self.screen.get_height() - 50),
        )
        self.player = player
        self.app.game_objects.append(StageBossOneMonster(self.app))
        all_sprites.add(player)

        while self.is_playing:
            print(self.app.game_objects.__len__())
            delta_time = self.app.clock.tick(self.app.fps)
            self.app.delta_time = delta_time
            player.delta_time = delta_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.on_event_keydown(event.key)
                    if event.key == pygame.K_RIGHT:
                        player.on_event_keydown(event.key)
                    if event.key == pygame.K_UP:
                        player.on_event_keydown(event.key)
                    if event.key == pygame.K_DOWN:
                        player.on_event_keydown(event.key)
                if event.type == pygame.KEYUP:
                    if (
                            event.key == pygame.K_LEFT
                            or event.key == pygame.K_RIGHT
                            or event.key == pygame.K_UP
                            or event.key == pygame.K_DOWN
                    ):
                        player.on_event_keyup(event.key)

                if event.type == monster_create_event:
                    self.spawn_monster()

            # display background
            bg: pygame.Surface = self.image["bg-stage3"]

            bg_base_y_position = bg_y
            self.screen.blit(bg, (0, -bg.get_height() + bg_base_y_position))
            self.screen.blit(bg, (0, bg_base_y_position))
            self.screen.blit(bg, (0, bg.get_height() + bg_base_y_position))
            if bg_y >= bg.get_height():
                bg_y = 0
            bg_y += 1

            # player 사망처리
            if player.is_destroyed:
                self.is_playing = False
                self.audio["bgm_till_the_end_of_infinity.mp3"].stop()
                self.app.select_scene(1)
                self.app.current_scene.__init__()

            # 최상단 Layer , UI같은거
            hp_img = self.app.image["ui/hp.png"]
            hp_img = pygame.transform.scale(hp_img, (25, 25))
            hp_img_position = (0, self.screen.get_height() - hp_img.get_height())
            self.screen.blit(hp_img, hp_img_position)
            hp_text = font.render(f"x{player.current_hp}", True, (255, 255, 255))
            self.screen.blit(
                hp_text,
                (
                    hp_img_position[0] + hp_img.get_width() - hp_text.get_width(),
                    hp_img_position[1] + hp_img.get_height() - hp_text.get_height(),
                ),
            )

            score_text = ptext.draw(
                f"Score:{self.data['score']}",
                (-99, -99),
                owidth=1.1,
                ocolor=(255, 255, 255),
                color=(0, 0, 0),
                fontname=MAPLE_STORY_BOLD_FONT,
                fontsize=18
            )
            self.screen.blit(score_text[0], (0, 0))

            gold_text = ptext.draw(
                f"{self.data['gold']}g",
                (-99, -99),
                owidth=1.1,
                ocolor=(255, 255, 255),
                color=(0, 0, 0),
                fontname=MAPLE_STORY_BOLD_FONT,
                fontsize=18
            )
            self.screen.blit(gold_text[0], (self.screen.get_width() - gold_text[0].get_width(), 0))

            #
            self.elapsed_frame += 1

            all_sprites.update()
            for game_object in self.app.game_objects:
                game_object.update()
                if game_object.is_destroyed:
                    try:
                        self.app.game_objects.remove(game_object)
                    except:  # Exception as exception:
                        pass

            for sprite in all_sprites:
                self.screen.blit(sprite.image, (sprite.position[0], sprite.position[1]))
            pygame.display.update()

    def spawn_monster(self):
        monster_img = self.image["monsters/candy.png"]
        monster = MonsterCandy(
            image=monster_img,
            arrow_image=self.image["monsters/candy_arrow.png"],
            position=(
                randrange(0, self.screen.get_width() - monster_img.get_width()),
                0,
            ),
            app=self.application,
            check_colliders=[self.player]
        )

        self.app.game_objects.append(monster)
