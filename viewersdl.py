__author__ = 'Geoffrey Frogeye; RAEON'

from time import time, sleep
import sdl2.ext
import sdl2.sdlgfx

BLACK = sdl2.ext.Color(0, 0, 0)

class GameViewer(object):

    def __init__(self, game):
        self.game = game

        # initialize sdl
        sdl2.ext.init()

        # window
        self.resolution = self.width, self.height = 800, 800
        self.window = sdl2.ext.Window("pygar", size=self.resolution)
        self.context = sdl2.ext.Renderer(self.window)

        # objects
        self.factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        self.cells = dict()

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
        scale = self.game.view_w / self.width
        scale = scale or 2

        # events
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                return False
            elif event.type == sdl2.SDL_MOUSEMOTION:
                x, y = event.motion.x, event.motion.y
                x *= scale
                y *= scale
                for bot in self.game.bots:
                    bot.send_move(x, y)
            elif event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_w:
                    for bot in self.game.bots:
                        bot.send_throw(1)
                elif event.key.keysym.sym == sdl2.SDLK_SPACE:
                    for bot in self.game.bots:
                        bot.send_split(1)
                elif event.key.keysym.sym == sdl2.SDLK_r:
                    for bot in self.game.bots:
                        bot.send_spawn()
            #     elif event.key.keysym.sym == sdl2.SDL_K_f:
            #         self.render_special = True
            # elif event.type == KEYUP:
            #     if event.key == K_f:
            #         self.render_special = False


        # clear screen
        # sdl2.ext.fill(self.renderer.surface, BLACK)

        # draw cells
        self.context.clear(0)
        values = self.game.cells.copy().values()
        for cell in values:
            # color = sdl2.ext.Color(cell.color[0], cell.color[1], cell.color[2], 255)
            color = 0xFF << 24 | cell.color[2] << 16 | cell.color[1] << 8 | cell.color[0]
            sdl2.sdlgfx.filledCircleColor(self.context.renderer,
                                          int((cell.x) / scale),
                                          int((cell.y) / scale),
                                          int(cell.size / scale) or 1,
                                          color)

        # render
        self.context.present()
        # self.window.refresh()

        return True


if __name__ == '__main__':
    g = GameViewer(None)
    g.run()
