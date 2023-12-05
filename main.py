from pico2d import open_canvas, delay, close_canvas
import game_framework
import logo_mode
import play_mode as start_mode
import play_mode as start_mode, logo_mode

open_canvas(1000, 600)
game_framework.run(logo_mode)
close_canvas()

