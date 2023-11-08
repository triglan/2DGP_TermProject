from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('Resource\Court2.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(500, 300)
        #self.image.clip_draw(500, 500, 500, 500, 500, 500)



