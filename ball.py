from pico2d import *
import game_world
import game_framework

BALL_WID = 30
BALL_HEI = 30
class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 300, angle = 45.0):
        if Ball.image == None:
            Ball.image = load_image('Resource/badminton_ball.png')
        self.x, self.y, self.velocity, self.angle = x, y, velocity, angle
        self.x0, self.y0 = x, y
        self.gravity = 10

    def draw(self):
        #self.image.draw(self.x, self.y)
        self.image.clip_composite_draw(0, 0, 950, 730, 0, '',
                                       self.x, self.y, BALL_WID, BALL_HEI)
        draw_rectangle(*self.get_bb())

    def update(self):
        radianAngle = math.radians(self.angle)
        self.x += self.velocity * game_framework.frame_time * math.cos(radianAngle)
        self.y += self.velocity * game_framework.frame_time * math.sin(radianAngle)
        if(self.angle > -90):
            self.angle -= 0.2
        print(self.angle)
        if self.x < 25 or self.x > 1000 - 25:
            self.velocity = -self.velocity
            print(f'turn back')
        if self.y < 100:#땅에 부딪치면 삭제
            game_world.remove_object(self)



    # fill here
    def get_bb(self):
        return self.x - BALL_WID / 2, self.y - BALL_WID / 2, self.x + BALL_WID / 2, self.y + BALL_WID / 2

    def handle_collision(self, group, other):
        if group == 'boy:ball':
            game_world.remove_object(self)
