from pico2d import *
import game_world
import game_framework

pi = 3.141592

class Racket:
    image = None

    def __init__(self, x = 400, y = 300, rad = 0):
        if Racket.image == None:
            Racket.image = load_image('Resource/racket1.png')
        self.x, self.y, self.rotate = x-20, y, rad

    def draw(self):
        #self.image.draw(self.x, self.y)
        self.image.clip_composite_draw(0, 0, 500, 500, -self.rotate / 180 * pi, 'h', self.x, self.y, 100, 100)
        #self.image.clip_composite_draw(0, 0, 500, 500, 1, 'h', self.x, self.y, 100, 100)
        #draw_rectangle(*self.get_bb())

    def update(self):
        self.rotate += 200 * game_framework.frame_time
        self.y += 40 * game_framework.frame_time
        self.x += 40 * game_framework.frame_time
        print(f'{self.rotate}')
        if self.rotate >= 0:
            game_world.remove_object(self)

    # fill here
    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if group == 'boy:ball':
            game_world.remove_object(self)
