import random

from pico2d import *
import game_framework

import game_world
import title_mode
from background import BackGround, special_BackGround
from badminton_player import Badminton_player
from badminton_enemy import Badminton_enemy
from ball import Ball

# player = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            player.handle_event(event)

def init():
    global background
    global player
    global balls

    running = True

    background = BackGround()
    game_world.add_object(background, 0)

    special_background = special_BackGround()
    game_world.add_object(special_background, 3)

    player = Badminton_player()
    game_world.add_object(player, 1)
    game_world.add_collision_pair('player:ball', player, None)#플레이어와 공 충돌

    enemy = Badminton_enemy()
    game_world.add_object(enemy, 1)
    game_world.add_collision_pair('enemy:ball', enemy, None)#플레이어와 공 충돌


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()
    # fill here
    # for ball in balls:
    #     if game_world.collide(player, ball):
    #         print("COLLISION player:ball")

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

