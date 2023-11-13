import random

from pico2d import *
import game_framework

import game_world
from background import Grass
from badminton_player import Badminton_player
from ball import Ball

# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global grass
    global boy
    global balls

    running = True

    grass = Grass()
    game_world.add_object(grass, 0)

    boy = Badminton_player()
    game_world.add_object(boy, 1)





def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()
    # fill here
    # for ball in balls:
    #     if game_world.collide(boy, ball):
    #         print("COLLISION boy:ball")

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

