# 이것은 각 상태들을 객체로 구현한 것임.
from random import randint

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    SDLK_l, \
    draw_rectangle, load_music, load_wav
from sdl2 import SDLK_r, SDLK_z

from ball import Ball
import game_world
import game_framework
import config

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
        player.x += player.dir * config.PLAYER_RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(25, player.x, 500-25)
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4


    @staticmethod
    def draw(player):
        if player.face_dir == -1:
            player.walking_image.clip_composite_draw(int(player.frame) * 22, 0, 22, 25, 0, 'h', player.x, player.y, PLAYER_WID, PLAYER_HEI)
            if player.isDash:
                player.dash_image.clip_composite_draw(0, 0, 1920, 1080, 0, '', player.x + 40, player.y + 20, PLAYER_WID * 3, PLAYER_HEI * 2)
        else:
            player.walking_image.clip_composite_draw(int(player.frame) * 22, 0, 22, 25, 0, '', player.x, player.y, PLAYER_WID, PLAYER_HEI)
            if player.isDash:
                player.dash_image.clip_composite_draw(0, 0, 1920, 1080, 0, 'h', player.x - 40, player.y + 20, PLAYER_WID * 3, PLAYER_HEI * 2)


class Swing:
    @staticmethod
    def enter(player, e):#key_down시 Run하게끔 key_up시 다시 Idle로 바꿔주기
        if right_down(e): # 오른쪽으로 RUN
            player.dir,  player.face_dir = 1, 1
            return
        elif left_down(e): # 왼쪽으로 RUN
            player.dir,  player.face_dir = -1, -1
            return
        if left_up(e) or right_up(e):
            player.dir = 0
            return
        player.frame = 0
        player.swinging = True
        print(f'player dir : {player.dir}')
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time / 3) % 4#너무 빨라서 애니메이션 재생 느리게 함
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
        player.swing_image.clip_composite_draw(int(player.frame) * 21, 0, 21, 25, 0, '', player.x, player.y, PLAYER_WID, PLAYER_HEI)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Swing},
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
        self.swing_image = load_image('Resource/mario_swing.png')
        self.dash_image = load_image('Resource/dash.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.swinging = False
        self.ball = None

        self.player_score_font = load_font('ENCR10B.TTF', 25)
        self.player_score_color = (255, 255, 255)  # 폰트 색상 (흰색)
        self.hit_sound = load_wav('Sounds/hit1.mp3')
        self.hit_sound.set_volume(30)
        self.dash_sound = load_wav('Sounds/dash.mp3')
        self.dash_sound.set_volume(30)

        self.dash_start_time = get_time()
        self.isDash = False

    def swing(self):
        if not config.isServed and config.isPlayerTurn:
            config.isServed = True
            config.isPlayerTurn = False
            self.hit_sound.play()
            self.ball = Ball(self.x, self.y, config.BALL_SPEED_PPS, randint(25, 50))# randint(30, 50)
            game_world.add_object(self.ball)
            game_world.add_collision_pair('player:ball', None, self.ball)
            game_world.add_collision_pair('enemy:ball', None, self.ball)

    def update(self):
        self.state_machine.update()
        if self.isDash:
            self.dash()

    def dash(self):
        if get_time() - self.dash_start_time < 0.25:
            print(f'dash')
            config.PLAYER_RUN_SPEED_PPS = 30 * config.PIXEL_PER_KMPH
        else:
            config.PLAYER_RUN_SPEED_PPS = 15 * config.PIXEL_PER_KMPH
            self.isDash = False


    def handle_event(self, event):
        if config.GameOver and event.type == SDL_KEYDOWN and event.key == SDLK_r:
            self.reset_game()  # Define the reset_game function separately
        if event.type == SDL_KEYDOWN and event.key == SDLK_z:
            self.isDash = True
            self.dash_start_time = get_time()
            self.dash_sound.play()

        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        #self.font.draw(self.x-10, self.y + 50, f'{self.ball_count:02d}', (255, 255, 0)) # 글자 출력
        draw_rectangle(*self.get_bb()) # 튜플을 풀어해쳐서 분리해서 인자로 제공 충돌체

        self.player_score_font.draw(200, 70, f'Player Score : {config.player_score}', self.player_score_color)
        self.player_score_font.draw(500, 70, f'Enemy Score : {config.enemy_score}', self.player_score_color)
        self.player_score_font.draw(0, 25, f'<- -> : move z : dash space : serve, hit', self.player_score_color)


    # fill here
    def get_bb(self):#bounding box
        return self.x,  self.y - 30, self.x + 50,  self.y + 30

    def handle_collision(self, group, other):
        if group == 'player:ball' and config.isPlayerTurn and self.swinging: # 충돌 시, 플레이어 턴 휘두루는 중이면
            config.change_ball_dir = True
            config.isPlayerTurn = False
            config.changeAI = True
            self.hit_sound.play()
            print('충돌함')

    def reset_game(self):
        config.change_ball_dir = False
        config.isPlayerTurn = True  # 플레이어가 치면 True enemy가 치면 False
        config.isServed = False
        config.changeAI = True
        config.AIServeTimer = 0.0
        config.player_score = 0
        config.enemy_score = 0
        config.isServed = False
        config.player_score = 0
        config.enemy_score = 0
        config.stage_num = 1
        config.change_image = False
        config.clear_timer = 0.0
        config.CLEARSCORE = 3
        config.wait_round = False
        config.PLAYER_RUN_SPEED_PPS = 20 * config.PIXEL_PER_KMPH
        config.BALL_SPEED_PPS = 40 * config.PIXEL_PER_KMPH
        config.BALL_ADD_VEL = 2 * config.PIXEL_PER_KMPH
        config.reset_enemy = True
        config.reset_ball = True
        config.GameOver = False
        config.newbgm = load_music('Sounds\stage1.mp3')
        config.newbgm.set_volume(30)
        config.newbgm.repeat_play()
        config.clearbgm = True