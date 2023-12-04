PIXEL_PER_KMPH = 18.518
change_ball_dir = False
isPlayerTurn = True # 플레이어가 치면 True enemy가 치면 False
isServed = False
changeAI = True

ball_angle = 0.0
ball_vel = 0.0
ball_x, ball_y = 0.0, 0.0
AIServeTimer = 0.0

player_score = 0
enemy_score = 0
stage_num = 1

change_image = False

clear_timer = 0.0
CLEARSCORE = 3

GameOver = False
clearbgm = True

wait_round = False
reset_enemy = False
reset_ball = False
gameClear = False

# player Run Speed
PLAYER_RUN_SPEED_PPS = 15 * PIXEL_PER_KMPH
#ball Speed
BALL_SPEED_PPS = 40 * PIXEL_PER_KMPH
BALL_ADD_VEL = 2 * PIXEL_PER_KMPH # 2km/h

newbgm = None