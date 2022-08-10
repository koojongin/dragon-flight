import sys
from random import randrange

import pygame

from src.interfaces.i_application import IApplication
from src.objects.monster import Monster
from src.objects.player import Player
from src.scenes.scene import GameScene


class StageScene(GameScene):
    bg_y_position = 0
    elapsed_frame = 0

    def __init__(self, application: IApplication):
        self.application = application
        self.app = self.application
        self.screen = self.application.screen
        self.image = self.application.image
        self.audio = self.application.audio

    def play(self):
        self.audio["bgm_fortress_sky"].set_volume(0.5)
        self.audio["bgm_fortress_sky"].play(-1)

        # values
        bg_y = 0
        monsters = [
            Monster(
                image=self.image["monsters/candy.png"],
                arrow_image=self.image["monsters/candy_arrow.png"],
                position=(100, 0)
            )
        ]

        monster_create_event = pygame.USEREVENT + 1
        pygame.time.set_timer(monster_create_event, 941)
        all_sprites = pygame.sprite.Group()
        player = Player(
            self.image["monsters/candy.png"],
            app=self.app,
            position=(0, self.screen.get_height() - 50),
        )
        all_sprites.add(player)

        while True:
            delta_time = self.app.clock.tick(self.app.fps)
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
                    monsters.append(Monster(
                        image=self.image["monsters/candy.png"],
                        arrow_image=self.image["monsters/candy_arrow.png"],
                        position=(randrange(0, self.screen.get_width()), 0)
                    ))

            # display background
            bg: pygame.Surface = self.image["bg-stage3"]

            bg_base_y_position = bg_y
            self.screen.blit(bg, (0, -bg.get_height() + bg_base_y_position))
            self.screen.blit(bg, (0, bg_base_y_position))
            self.screen.blit(bg, (0, bg.get_height() + bg_base_y_position))
            if bg_y >= bg.get_height():
                bg_y = 0
            bg_y += 1

            # display monsters
            for monster_index, monster in enumerate(monsters):
                if monster.is_destroy is True:
                    monsters.remove(monster)
                    continue
                self.screen.blit(monster.image, (monster.x, monster.y))
                if monster.bullet_cooldown_count <= 0:
                    monster.fire(
                        (
                            player.x + player.rect.width / 2,
                            player.y + player.rect.height / 2,
                        )
                    )
                    monster.bullet_cooldown_count = monster.bullet_cooldown
                monster.y += monster.speed * delta_time
                if monster.y > self.screen.get_height():
                    monsters.remove(monster)
                    continue

                monster.bullet_cooldown_count -= delta_time

                for bullet in monster.bullets:
                    self.screen.blit(bullet.image, (bullet.x, bullet.y))
                    bullet.update(self, delta_time)
                    if bullet.is_destroy is True:
                        monster.bullets.remove(bullet)

            # display player
            if player.missile_cooldown_count <= 0:
                player.fire()
                player.missile_cooldown_count = player.missile_cooldown
            player.missile_cooldown_count -= delta_time

            for missile in player.missiles:
                self.screen.blit(missile.image, (missile.x, missile.y))
                missile.update(self, delta_time)
                if missile.is_destroy is True:
                    player.missiles.remove(missile)

            #
            self.elapsed_frame += 1

            all_sprites.update()
            all_sprites.draw(self.screen)
            pygame.display.update()
