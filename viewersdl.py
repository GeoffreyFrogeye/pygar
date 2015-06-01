__author__ = 'Geoffrey Frogeye'

import sdl2.ext
from time import time, sleep

# sdl2.ext.init()
#
# processor = sdl2.ext.TestEventProcessor()
# processor.run(window)

class GameViewer(object):

    def __init__(self, game):
        self.game = game

        # initialize sdl
        sdl2.ext.init()

        # window
        self.resolution = self.width, self.height = 800, 800
        self.window = sdl2.ext.Window("Hello World!", size=self.resolution)

        # fps
        self.frames = 0
        self.last_frames = 0
        self.timer = 0

        self.window.show()

    def run(self):
        while self.render():
            pass
        sdl2.ext.quit()

    def render(self):
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                return False

        # flip buffers
        self.window.refresh()

        return True


if __name__ == '__main__':
    g = GameViewer(None)
    g.run()
