# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    draw_rectangle
from ball import Ball
import game_world
import game_framework
from racket import Racket


# state event check
# ( state event type, event value )

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




# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
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
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        if get_time() - player.wait_time > 2:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        if boy.face_dir == -1:
            boy.idle_image.clip_composite_draw(int(boy.frame) * 20, 0, 20, 25, 0, 'h', boy.x, boy.y, PLAYER_WID, PLAYER_HEI)
        else:
            boy.idle_image.clip_composite_draw(int(boy.frame) * 20, 0, 20, 25, 0, '', boy.x, boy.y, PLAYER_WID, PLAYER_HEI)



class Run:
    @staticmethod
    def enter(boy, e):
        if dir == 0 and (left_up(e) or right_up(e)):
            boy.state_machine.handle_event(('TIME_OUT', 0))
            print(f'comein')

        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            boy.dir,  boy.face_dir = 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            boy.dir,  boy.face_dir = -1, -1
            print(f'whyhere')

    @staticmethod
    def exit(boy, e):
        #boy.dir = 0
        pass

    @staticmethod
    def do(boy):
        boy.x += boy.dir * RUN_SPEED_PPS * game_framework.frame_time
        boy.x = clamp(25, boy.x, 500-25)
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4


    @staticmethod
    def draw(boy):
        if boy.face_dir == -1:
            boy.walking_image.clip_composite_draw(int(boy.frame) * 22, 0, 22, 25, 0, 'h', boy.x, boy.y, PLAYER_WID, PLAYER_HEI)
        else:
            boy.walking_image.clip_composite_draw(int(boy.frame) * 22, 0, 22, 25, 0, '', boy.x, boy.y, PLAYER_WID, PLAYER_HEI)


class Swing:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            boy.dir,  boy.face_dir = 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            boy.dir,  boy.face_dir = -1, -1
        boy.frame = 0
        pass

    @staticmethod
    def exit(boy, e):
        pass



    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time / 5) % 4#너무 빨라서 애니메이션 재생 느리게 함
        if boy.frame >= 3:
            if boy.dir == 1:
                boy.state_machine.handle_event(('TIME_OUT_WHILE_RUNNING', 0))  # 오른쪽으로 달리기
            elif boy.dir == -1:
                boy.state_machine.handle_event(('TIME_OUT_WHILE_RUNNING', 0))  # 왼쪽으로 달리기
            else:
                boy.state_machine.handle_event(('TIME_OUT', 0))  # Idle 상태로 전환

    @staticmethod
    def draw(boy):
        if boy.face_dir == -1:
            boy.swing_image.clip_composite_draw(int(boy.frame) * 21, 0, 21, 25, 0, 'h', boy.x, boy.y, PLAYER_WID, PLAYER_HEI)
        else:
            boy.swing_image.clip_composite_draw(int(boy.frame) * 21, 0, 21, 25, 0, '', boy.x, boy.y, PLAYER_WID, PLAYER_HEI)

class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Swing},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Swing},
            Swing: {right_down: Swing, left_down: Swing, left_up: Swing, right_up: Swing, time_out: Idle, time_out_while_running: Run},
        }

    def start(self):
        self.cur_state.enter(self.boy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.boy)





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
        self.round_start = True



    def swing(self):
        pass
        # if self.ball_count > 0:
        #     self.ball_count -= 1
        #     racket = Racket(self.x, self.y + 30, -90)
        #     game_world.add_object(racket)

    def update(self):
        self.state_machine.update()

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
        pass