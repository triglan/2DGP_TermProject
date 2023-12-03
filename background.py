from pico2d import *

import config
import game_framework


class BackGround:
    def __init__(self):
        self.stage1 = load_image('Resource\Court1.png')
        self.stage2 = load_image('Resource\Court2.png')
        self.stage3 = load_image('Resource\Court3.png')

    def update(self):
        pass

    def draw(self):
        if config.stage_num == 1:
            self.stage1.draw(500, 300)
        if config.stage_num == 2:
            self.stage2.draw(500, 300)
        if config.stage_num == 3:
            self.stage3.draw(500, 300)


start_time = False

class special_BackGround:
    def __init__(self):
        self.clearimage = load_image('Resource\StageClear.png')
        self.overimage = load_image('Resource\gameOver.jpg')
        self.start_time = False
        self.win_start_time = None
    def update(self):
        if config.player_score >= config.CLEARSCORE:
            config.player_score = 0
            config.enemy_score = 0
            config.wait_round = True
            self.win_start_time = get_time()

            print(f'get time : {get_time()} start : {self.win_start_time}')

        if config.wait_round:
            if get_time() - self.win_start_time > 2:
                config.stage_num += 1
                config.wait_round = False
                config.change_image = True
                config.isPlayerTurn = True
                config.isServed = False
                config.changeAI = True
                if config.stage_num == 2:
                    config.BALL_SPEED_PPS = 50 * 9.259 # 시속 50km, 적 이속도 추가 부탁
                elif config.stage_num == 3:
                    config.BALL_SPEED_PPS = 70 * 9.259  # 시속 70km


    def draw(self):
        if config.wait_round == True:
            self.clearimage.draw(500, 300)
        elif config.enemy_score >= config.CLEARSCORE:
            self.overimage.draw(500, 300)


