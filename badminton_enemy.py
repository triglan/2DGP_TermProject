# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_l , \
    draw_rectangle
from ball import Ball
import game_world
import game_framework
import config

from racket import Racket


# state event check
# ( state event type, event value )



# player Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

PLAYER_WID = 50
PLAYER_HEI = 100



class Badminton_enemy:
    def __init__(self):
        self.x, self.y = 200, 150
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.walking_image = load_image('Resource/mario_walking.png')
        self.idle_image = load_image('Resource/mario_Idle.png')
        self.swing_image = load_image('Resource/mario_swing.gif')
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine.start()
        self.isServed = False
        self.isServedCool = False
        self.cooldown = 0.0
        self.swinging = False



    def swing(self):
        pass
        if not self.isServed:
            self.isServedCool = True
            self.cooldown = 0.0
            ball = Ball(self.x, self.y, self.face_dir * 300)
            game_world.add_object(ball)
            game_world.add_collision_pair('enemy:ball', None, ball)

    def update(self):
        self.state_machine.update()
        print(f'{self.swinging}')
        if self.isServedCool:
            self.cooldown += game_framework.frame_time
            if self.cooldown > 1:
                self.isServed = True


    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        #self.font.draw(self.x-10, self.y + 50, f'{self.ball_count:02d}', (255, 255, 0)) # 글자 출력
        draw_rectangle(*self.get_bb()) # 튜플을 풀어해쳐서 분리해서 인자로 제공 충돌체

    # fill here
    def get_bb(self):#bounding box
        return self.x,  self.y - 30, self.x + 50,  self.y + 30

    def handle_collision(self, group, other):
        if group == 'player:ball':
            if self.isServed and self.swinging:
                config.change_ball_dir = True
                print('충돌함')