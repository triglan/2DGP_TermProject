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
CLEARSCORE = 1

wait_round = False

# player Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
PLAYER_RUN_SPEED_KMPH = 20.0  # Km / Hour
PLAYER_RUN_SPEED_MPM = (PLAYER_RUN_SPEED_KMPH * 1000.0 / 60.0)
PLAYER_RUN_SPEED_MPS = (PLAYER_RUN_SPEED_MPM / 60.0)
PLAYER_RUN_SPEED_PPS = (PLAYER_RUN_SPEED_MPS * PIXEL_PER_METER)

#ball Speed
BALL_SPEED_KMPH = 40.0  # Km / Hour
BALL_SPEED_MPM = (BALL_SPEED_KMPH * 1000.0 / 60.0)
BALL_SPEED_MPS = (BALL_SPEED_MPM / 60.0)
BALL_SPEED_PPS = (BALL_SPEED_MPS * PIXEL_PER_METER)
