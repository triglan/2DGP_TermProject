from random import randint

from pico2d import *

import config
import game_world
import game_framework
from config import change_ball_dir

BALL_WID = 30
BALL_HEI = 30
class Ball:
    image = None
    def __init__(self, x = 400, y = 300, velocity = config.BALL_SPEED_PPS, angle = 45.0, dir = 1):
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
        #draw_rectangle(*self.get_bb())

    def update(self):
        #print(f'angel : {self.angle} dir : {self.dir}, velocity : {self.velocity}')
        radianAngle = math.radians(self.angle)
        self.x += self.velocity * game_framework.frame_time * math.cos(radianAngle)
        self.y += self.velocity * game_framework.frame_time * math.sin(radianAngle)
        #self.velocity += game_framework.frame_time * 100
        if self.dir == 1:
            self.angle += -0.35
        elif self.dir == -1:
            self.angle += 0.35

        config.ball_angle = self.angle
        config.ball_vel = self.velocity
        config.ball_x = self.x
        config.ball_y = self.y

        # if config.reset_ball:
        #     game_world.remove_object(self)
        #     config.reset_ball=False

        if 499 < self.x and self.x < 501:#네트 검사
            if self.y < 200:#걸리면
                if self.dir == 1:# 우측, 즉 플레이어가 네트에 걸리면
                    config.isPlayerTurn = False
                    config.enemy_score += 1
                    config.changeAI = True
                else:
                    config.isPlayerTurn = True
                    config.player_score += 1
                    config.changeAI = True
                config.isServed = False
                config.AIServeTimer = 0
                game_world.remove_object(self)

        if self.x > 1000 - 25: # 벽과 충돌 시 죽이자 적벽에 충돌 시 패배
            self.change_direction(randint(225, 255), -1, self.velocity)
            config.changeAI = True
        elif self.x < 25: # 플레이어 벽과 충돌 시
            self.change_direction(randint(-80, -50), 1, self.velocity)
            config.changeAI = True

        if self.y < 100:#땅에 부딪치면 삭제
            if self.x < 500:#플레이어 땅에 떨어지면
                config.isPlayerTurn = False
                config.enemy_score += 1
                config.changeAI = True
            else:#상대 땅에 떨어지면
                config.isPlayerTurn = True
                config.player_score += 1
                config.changeAI = True
            config.isServed = False
            config.AIServeTimer = 0
            game_world.remove_object(self)

        if config.change_image:
            game_world.remove_object(self)


    # fill here
    def get_bb(self):
        return self.x - BALL_WID / 2, self.y - BALL_WID / 2, self.x + BALL_WID / 2, self.y + BALL_WID / 2

    def handle_collision(self, group, other):
        if group == 'player:ball':
            if config.change_ball_dir:
                self.change_direction(randint(20, 50), 1, self.velocity)
            config.changeAI = True
        if group == 'enemy:ball':
            self.change_direction(180 - randint(15, 60), -1,  self.velocity)
            config.changeAI = True

        change_ball_dir = False


    def change_direction(self, angle, dir, velocity = config.BALL_SPEED_PPS):
        self.angle = angle
        self.dir = dir
        self.velocity = velocity
        print(f'turn back')