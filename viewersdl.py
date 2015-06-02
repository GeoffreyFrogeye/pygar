__author__ = 'Geoffrey Frogeye'

import sdl2.ext
from time import time, sleep

BLACK = sdl2.ext.Color(0, 0, 0)

class GameViewer(object):

    def __init__(self, game):
        self.game = game

        # initialize sdl
        sdl2.ext.init()

        # window
        self.resolution = self.width, self.height = 800, 800
        self.window = sdl2.ext.Window("pygar", size=self.resolution)

        # rendering
        self.world = sdl2.ext.World()
        self.renderer = sdl2.ext.SoftwareSpriteRenderSystem(self.window)
        self.world.add_system(self.renderer)

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
            if event.type == sdl2.SDL_QUIT or event.type == sdl2.SDLK_ESCAPE:
                return False

        # draw
        sdl2.ext.fill(self.renderer.surface, BLACK)

        nothandled = list(cell for cell in self.cells)
        values = self.game.cells.copy().values()
        for cell in values:
            newsize = int(cell.size / scale) or 1
            newhalf = newsize / 2
            newpos = (int(cell.x / scale - newhalf), int(cell.y / scale - newhalf))
            if cell.id in self.cells: # If already on screen
                nothandled.remove(cell.id)
                sp_cell, wd_cell = self.cells[cell.id]
                if sp_cell.size[0] != newsize:
                    del sp_cell
                    sp_cell = self.factory.from_color(sdl2.ext.Color(*cell.color), size=(newsize, newsize))
                    wd_cell.sprite = sp_cell
                wd_cell.sprite.position = newpos
            else: # If new
                sp_cell = self.factory.from_color(sdl2.ext.Color(*cell.color), size=(newsize, newsize))
                wd_cell = sdl2.ext.Entity(self.world)
                wd_cell.sprite = sp_cell
                wd_cell.position = newpos
                # wd_cell = Cell(self.world, sp_cell, newpos[0], newpos[1])
                self.cells[cell.id] = (sp_cell, wd_cell)
        for cell in nothandled: # Deleting cells
            # TODO Use watchers
            sp_cell, wd_cell = self.cells[cell]
            del sp_cell
            wd_cell.delete()
            del self.cells[cell]

        # render
        self.world.process()
        self.window.refresh()

        return True


if __name__ == '__main__':
    g = GameViewer(None)
    g.run()
