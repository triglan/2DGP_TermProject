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
        self.overimage = load_image('Resource\gameOver.png')
        self.clear = load_image('Resource\GameClear.png')
        self.start_time = False
        self.win_start_time = None
        self.bgm1 = load_music('Sounds/stage1.mp3')
        self.bgm1.set_volume(30)
        self.bgm1.repeat_play()

        self.bgm2 = load_music('Sounds/stage2.mp3')
        self.bgm2.set_volume(30)

        self.bgm3 = load_music('Sounds/stage3.mp3')
        self.bgm3.set_volume(30)

        self.bgm = load_music('Sounds/Clear.mp3')
        self.bgm.set_volume(30)

        self.stage_clear = load_music('Sounds/nextRound.mp3')
        self.stage_clear.set_volume(30)

        self.game_over = load_music('Sounds/GameOver.mp3')
        self.game_over.set_volume(30)

    def update(self):
        if config.player_score >= config.CLEARSCORE:
            config.player_score = 0
            config.enemy_score = 0
            config.wait_round = True
            config.isServed = True
            self.win_start_time = get_time()
            self.stage_clear.play()
            if config.stage_num >= 3:
                self.stage_clear.set_volume(30)
                config.gameClear = True
                self.bgm.play()

            print(f'get time : {get_time()} start : {self.win_start_time}')
        if config.enemy_score >= config.CLEARSCORE:
            config.enemy_score = 0
            config.GameOver = True
            config.isServed = True
            config.isPlayerTurn = False
            self.stage_clear.set_volume(30)
            self.game_over.repeat_play()


        if config.wait_round and not config.GameOver:
            if get_time() - self.win_start_time > 3:
                config.stage_num += 1
                config.wait_round = False
                config.change_image = True
                config.isPlayerTurn = True
                config.isServed = False
                config.changeAI = True
                if config.stage_num == 2:
                    config.BALL_SPEED_PPS = 47 * config.PIXEL_PER_KMPH # 시속 50km, 적 이속도 추가 부탁
                    self.bgm2.repeat_play()

                elif config.stage_num == 3:
                    config.BALL_SPEED_PPS = 50 * config.PIXEL_PER_KMPH  # 시속 60km
                    self.bgm3.repeat_play()


        if config.gameClear:
            config.wait_round = True

    def draw(self):
        if config.wait_round == True:
            self.clearimage.draw(500, 300)
        elif config.GameOver:
            self.overimage.draw(500, 300)

        if config.gameClear:
            self.clear.draw(500, 300)


