# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_l , \
    draw_rectangle
from ball import Ball
import game_world
import game_framework
import config
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import play_mode
import math

from racket import Racket


# state event check
# ( state event type, event value )



# player Run Speed
PIXEL_PER_METER = (5.0 / 0.3)  # 10 pixel 30 cm
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
        self.x, self.y = 800, 150
        self.tx = 800
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.walking_image = load_image('Resource/mario_walking.png')
        self.idle_image = load_image('Resource/mario_Idle.png')
        self.swing_image = load_image('Resource/mario_swing.gif')
        self.font = load_font('ENCR10B.TTF', 16)
        self.isServed = False
        self.isServedCool = False
        self.cooldown = 0.0
        self.swinging = False
        self.move_speed = 0.0
        self.build_behavior_tree()

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.bt.run()


    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass


    def draw(self):
        self.idle_image.clip_composite_draw(int(self.frame) * 20, 0, 20, 25, 0, 'h', self.x, self.y, PLAYER_WID, PLAYER_HEI)
        draw_rectangle(*self.get_bb()) # 튜플을 풀어해쳐서 분리해서 인자로 제공 충돌체

    # fill here
    def get_bb(self):#bounding box
        return self.x,  self.y - 30, self.x + 50,  self.y + 30

    def move_slightly_to(self, tx):
        self.dir = math.atan2(0, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time

    def move_to(self, r = 0.5):
        self.move_slightly_to(self.tx)
        if (self.tx - self.x)**2 > r**2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_enemy_hit(self):
        pass

    def handle_collision(self, group, other):
        pass



    def set_target_location(self, x = None):
        if not x:
            raise ValueError('위치 지정을 해야 한다.')
        self.tx = x
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        a1 = Action('Set target location', self.set_target_location, 100) # action mode
        a2 = Action('Move to', self.move_to)
        root = SEL_chase_or_flee = Sequence('추적 또는 배회', a1, a2)

        self.bt = BehaviorTree(root)