# 이것은 각 상태들을 객체로 구현한 것임.
from random import randint

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_l , \
    draw_rectangle

from badminton_player import Badminton_player
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
PIXEL_PER_METER = (1.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

Enemy_WID = 50
Enemy_HEI = 100

animation_names = ['Walk', 'Idle', 'Hit']

class Badminton_enemy:
    def __init__(self):
        self.x, self.y = 750, 150
        self.tx = 750
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.walking_image = load_image('Resource/luigi_walking.png')
        self.idle_image = load_image('Resource/luigi_idle.png')
        self.swing_image = load_image('Resource/luigi_swing.gif')
        self.font = load_font('ENCR10B.TTF', 16)
        self.state = 'Idle'
        self.cooldown = 0.0
        self.swinging = False
        self.move_speed = 0.0
        self.build_behavior_tree()
        self.inHitbox = False
        self.hitting = False
        self.speed = RUN_SPEED_PPS

    def change_enemy_image(self):
        if config.stage_num == 2:
            self.walking_image = load_image('Resource/yoshi_walking.png')
            self.idle_image = load_image('Resource/yoshi_idle.png')
            self.swing_image = load_image('Resource/yoshi_swing.png')
        if config.stage_num == 3:
            self.walking_image = load_image('Resource/cupa_walking.png')
            self.idle_image = load_image('Resource/cupa_idle.png')
            self.swing_image = load_image('Resource/cupa_swing.png')
        self.tx = 750
        self.inHitbox = False
        self.hitting = False
        self.swinging = False
        self.state = 'Idle'
        self.x, self.y = 750, 150
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        config.change_image = False

    def update(self):
        if not config.wait_round:
            if self.state == 'Idle': self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
            elif self.state == 'Walk': self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
            elif self.state == 'Hit': self.frame = (self.frame + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) / 5) % 4
            #(f'state : {self.state}  frame : {self.frame} hitting : {self.hitting} first {self.inHitbox}')
            print(f'lccate x : {self.tx}  // isPlayerTurn : {config.isPlayerTurn} // isServed : {config.isServed}')

            if config.change_image:
                self.change_enemy_image()

            self.find_target_location()
            if not config.isPlayerTurn and not config.isServed:#서브 넣기
                config.AIServeTimer += game_framework.frame_time
                self.state = 'Idle'
                self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
                if(config.AIServeTimer >= 2):
                    config.isServed = True
                    config.isPlayerTurn = True
                    self.ball = Ball(self.x, self.y, config.BALL_SPEED_PPS, randint(120, 160), -1)
                    game_world.add_object(self.ball)
                    game_world.add_collision_pair('player:ball', None, self.ball)
                    game_world.add_collision_pair('enemy:ball', None, self.ball)
            else:
                self.bt.run()


    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass


    def draw(self):
        if(self.state == 'Idle'):
            self.idle_image.clip_composite_draw(int(self.frame) * 20, 0, 20, 25, 0, 'h', self.x, self.y, Enemy_WID, Enemy_HEI)
        elif(self.state == 'Walk'):
            if self.face_dir == -1: self.walking_image.clip_composite_draw(int(self.frame) * 22, 0, 22, 25, 0, 'h', self.x, self.y, Enemy_WID, Enemy_HEI)
            else: self.walking_image.clip_composite_draw(int(self.frame) * 22, 0, 22, 25, 0, '', self.x, self.y, Enemy_WID, Enemy_HEI)
        elif(self.state == 'Hit'):
            self.swing_image.clip_composite_draw(int(self.frame) * 21, 0, 21, 25, 0, 'h', self.x, self.y, Enemy_WID, Enemy_HEI)

        draw_rectangle(*self.get_bb()) # 튜플을 풀어해쳐서 분리해서 인자로 제공 충돌체


    # fill here
    def get_bb(self):#bounding box
        return self.x - 50,  self.y - 30, self.x,  self.y + 30

    def move_slightly_to(self, tx):
        self.dir = math.atan2(0, tx - self.x)
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time

    def move_to(self):
        self.move_slightly_to(self.tx)
        self.state = 'Walk'


    def hit(self):
        if not self.hitting:
            self.hitting = True
            self.frame = 0
            ball = Ball(self.x, self.y, config.BALL_SPEED_PPS)
        if self.hitting:
            self.state = 'Hit'
            if self.frame >= 3:
                self.hitting = False

    def idle(self):
        self.state = 'Idle'

    def handle_collision(self, group, other):
        if group == 'enemy:ball':
            self.inHitbox = True
            config.isPlayerTurn = True

    def set_target_location(self):
        if not self.tx:
            raise ValueError('위치 지정을 해야 한다.')
        if(self.tx > self.x): self.face_dir = 1
        else: self.face_dir = -1
        if (self.tx - self.x)**2 > 0.5 ** 2: return BehaviorTree.SUCCESS
        else: return BehaviorTree.FAIL

    def is_HitBox(self): # 조건식하고 해당 프레임동안 hit 켜주기
        if self.inHitbox or self.hitting:
            self.inHitbox = False
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def find_target_location(self):
        if config.isServed and config.changeAI:
            config.changeAI = False
            if not config.isPlayerTurn: #AI가 쳤으면 pass, 플레이어가 치면 고고
                target_x, target_y, target_angle = config.ball_x, config.ball_y, config.ball_angle
                while target_y >= 100: # 4.5m, 캐릭터 중심위치까지 검사
                    radianAngle = math.radians(target_angle)
                    target_x += config.ball_vel * game_framework.frame_time * math.cos(math.radians(radianAngle))
                    target_y += config.ball_vel * game_framework.frame_time * math.sin(math.radians(radianAngle))
                    target_angle -= 0.1
                self.tx = clamp(550, target_x, 950)
            else:
                self.tx = 750 # 22.5m



    def build_behavior_tree(self):
        TargetCon = Condition('Set target location', self.set_target_location) # AI턴에 위치에 도착하지 않았다면 이동
        MovetoAction = Action('Move to', self.move_to)
        HitAction = Action('hit', self.hit)
        IdleAction = Action('Idle', self.idle)

        IsHitBoxCon = Condition('Is in Hit Box?', self.is_HitBox)

        SEQ_find_move = Sequence('탐색 및 이동', TargetCon, MovetoAction)
        SEQ_Hit = Sequence('히트 가능 시 히트', IsHitBoxCon, HitAction)

        SEL_AI = Selector('히트 이동 아이들', SEQ_Hit, SEQ_find_move, IdleAction)

        root = SEL_AI
        self.bt = BehaviorTree(root)