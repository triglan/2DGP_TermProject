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

def l_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_l

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

def time_out_while_running(e):
    return e[0] == 'TIME_OUT_WHILE_RUNNING'

# time_out = lambda e : e[0] == 'TIME_OUT'




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


class Idle:
    @staticmethod
    def enter(player, e):
        player.dir = 0
        player.frame = 0
        player.wait_time = get_time() # pico2d import 필요
        if l_down(e):
            ball = Ball(900, 100, 300, 135, -1)
            game_world.add_object(ball)
            game_world.add_collision_pair('player:ball', None, ball)

    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.swing()
    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        if get_time() - player.wait_time > 2:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.face_dir == -1:
            player.idle_image.clip_composite_draw(int(player.frame) * 20, 0, 20, 25, 0, 'h', player.x, player.y, PLAYER_WID, PLAYER_HEI)
        else:
            player.idle_image.clip_composite_draw(int(player.frame) * 20, 0, 20, 25, 0, '', player.x, player.y, PLAYER_WID, PLAYER_HEI)



class Run:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir,  player.face_dir = 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir,  player.face_dir = -1, -1

    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.swing()
        pass

    @staticmethod
    def do(player):
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(25, player.x, 500-25)
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4


    @staticmethod
    def draw(player):
        if player.face_dir == -1:
            player.walking_image.clip_composite_draw(int(player.frame) * 22, 0, 22, 25, 0, 'h', player.x, player.y, PLAYER_WID, PLAYER_HEI)
        else:
            player.walking_image.clip_composite_draw(int(player.frame) * 22, 0, 22, 25, 0, '', player.x, player.y, PLAYER_WID, PLAYER_HEI)


class Swing:
    @staticmethod
    def enter(player, e):#key_down시 Run하게끔 key_up시 다시 Idle로 바꿔주기
        if right_down(e): # 오른쪽으로 RUN
            player.dir,  player.face_dir = 1, 1
        elif left_down(e): # 왼쪽으로 RUN
            player.dir,  player.face_dir = -1, -1
        if left_up(e) or right_up(e):
            player.dir = 0
        player.frame = 0
        player.swinging = True
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time / 5) % 4#너무 빨라서 애니메이션 재생 느리게 함
        if player.frame >= 3:
            player.swinging = False
            config.change_ball_dir = False
            if player.dir == 1:
                player.state_machine.handle_event(('TIME_OUT_WHILE_RUNNING', 0))  # 오른쪽으로 달리기
            elif player.dir == -1:
                player.state_machine.handle_event(('TIME_OUT_WHILE_RUNNING', 0))  # 왼쪽으로 달리기
            else:
                player.state_machine.handle_event(('TIME_OUT', 0))  # Idle 상태로 전환

    @staticmethod
    def draw(player):
        if player.face_dir == -1:
            player.swing_image.clip_composite_draw(int(player.frame) * 21, 0, 21, 25, 0, 'h', player.x, player.y, PLAYER_WID, PLAYER_HEI)
        else:
            player.swing_image.clip_composite_draw(int(player.frame) * 21, 0, 21, 25, 0, '', player.x, player.y, PLAYER_WID, PLAYER_HEI)

class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Swing, l_down: Idle},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Swing},
            Swing: {right_down: Swing, left_down: Swing, left_up: Swing, right_up: Swing, time_out: Idle, time_out_while_running: Run},
        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.player)





class Badminton_player:
    def __init__(self):
        self.x, self.y = 200, 150
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.walking_image = load_image('Resource/mario_walking.png')
        self.idle_image = load_image('Resource/mario_Idle.png')
        self.swing_image = load_image('Resource/mario_swing.gif')
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
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
            game_world.add_collision_pair('player:ball', None, ball)

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