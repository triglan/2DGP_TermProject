from pico2d import *
import game_world
import game_framework

BALL_WID = 30
BALL_HEI = 30
class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 300):
        if Ball.image == None:
            Ball.image = load_image('Resource/badminton_ball.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.gravity = 10

    def draw(self):
        #self.image.draw(self.x, self.y)
        self.image.clip_composite_draw(0, 0, 950, 730, 0, '',
                                       self.x, self.y, BALL_WID, BALL_HEI)
        draw_rectangle(*self.get_bb())

    def update(self):
        print(f'{game_framework.frame_time}')
        self.x += self.velocity * game_framework.frame_time
        accel = (self.velocity * game_framework.frame_time -
                                 0.5 * self.gravity * game_framework.frame_time ** 2)
        self.y += accel
        if self.x < 25 or self.x > 1000 - 25:
            self.velocity = -self.velocity
            print(f'turn back')
            #game_world.remove_object(self)



    # fill here
    def get_bb(self):
        return self.x - BALL_WID / 2, self.y - BALL_WID / 2, self.x + BALL_WID / 2, self.y + BALL_WID / 2

    def handle_collision(self, group, other):
        if group == 'boy:ball':
            game_world.remove_object(self)
