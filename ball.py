from pico2d import *

import config
import game_world
import game_framework
from config import change_ball_dir

BALL_WID = 30
BALL_HEI = 30
class Ball:
    image = None
    def __init__(self, x = 400, y = 300, velocity = 300, angle = 45.0, dir = 1):
        if Ball.image == None:
            Ball.image = load_image('Resource/badminton_ball.png')
        self.x, self.y, self.velocity, self.angle = x, y, velocity, angle
        self.can_change_dir = False
        self.dir = dir
        #dir 1일 시 우측, -1일시 좌측으로
        #우측일시 angle은 [90, -90], 좌측 이동시 [90, 270]

    def draw(self):
        #self.image.draw(self.x, self.y)
        self.image.clip_composite_draw(0, 0, 950, 730, 0, '',
                                       self.x, self.y, BALL_WID, BALL_HEI)
        draw_rectangle(*self.get_bb())

    def update(self):
        radianAngle = math.radians(self.angle)
        self.x += self.velocity * game_framework.frame_time * math.cos(radianAngle)
        self.y += self.velocity * game_framework.frame_time * math.sin(radianAngle)
        self.velocity += game_framework.frame_time * 100
        if self.dir == 1 and self.angle > -90:
            self.angle += -0.1
        elif self.dir == -1 and self.angle < 270:
            self.angle += 0.1

        if self.x > 1000 - 25 or self.x < 25: # 벽과 충돌 시
            self.change_direction(  180 - self.angle, -self.dir)
            print(self.angle)

        if self.y < 100:#땅에 부딪치면 삭제
            game_world.remove_object(self)



    # fill here
    def get_bb(self):
        return self.x - BALL_WID / 2, self.y - BALL_WID / 2, self.x + BALL_WID / 2, self.y + BALL_WID / 2

    def handle_collision(self, group, other):
        if group == 'player:ball':
            if config.change_ball_dir:
                if self.angle > 90:
                    self.change_direction(self.angle - 180, 1)
                else:
                    self.change_direction(180 - self.angle, -1)
                change_ball_dir = False


    def change_direction(self, angle, dir):
        self.angle = angle
        self.dir = dir
        print(f'turn back')