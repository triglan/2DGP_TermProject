from pico2d import load_image, get_events, clear_canvas, update_canvas, get_time
import game_framework
import play_mode
import title_mode


def init():
    global image
    global logo_start_time
    image = load_image('Resource/badminton_logo.png')
    logo_start_time = get_time()
    pass


def finish():
    pass


def handle_events():
    events = get_events()
    pass


def update():
    if get_time() - logo_start_time > 2:
        game_framework.change_mode(play_mode)
    pass


def draw():
    clear_canvas()
    image.draw(500, 300)
    update_canvas()
    pass


def pause():
    pass


def resume():
    pass