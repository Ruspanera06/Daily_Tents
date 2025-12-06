#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - https://tomamic.github.io/
@license This software is free - https://opensource.org/license/mit
"""

try:
    from __main__ import g2d
except:
    import g2d
from boardgame import BoardGame

W, H = 40, 40
DX, DY = 40, 40
BLACK, GRAY, WHITE, GREEN = (0, 0, 0), (127, 127, 127), (255, 255, 255), (0, 255, 0)

class BoardGameGui:
    def __init__(self, game: BoardGame,
                 actions={"LeftButton": "", "RightButton": "flag", "g": "automate_green", "t":"automate_tents"},
                 annots={"#": (GRAY, 0), "!": (GRAY, 2)}):
        self._game = game
        self._actions = actions
        self._annots = annots
        self.update_buttons()

    def tick(self):
        game = self._game
        mouse_x, mouse_y = g2d.mouse_pos()
        x, y = (mouse_x-DX) // W, (mouse_y-DY) // H
        released = set(g2d.previous_keys()) - set(g2d.current_keys())
        if game.finished():
            g2d.alert(game.status())
            g2d.close_canvas()
            return
        if "Escape" in released:  # "Escape" key released
            g2d.close_canvas()
            return
        for k, v in self._actions.items():
            if k in released and y < game.rows():
                game.play(x, y, v)
                self.update_buttons((x, y))

    def update_buttons(self, last_move=None):
        cols, rows = self._game.cols(), self._game.rows()
        g2d.clear_canvas(BLACK)
        self.draw_nums_tents(cols, rows)
        for y in range(rows):
            for x in range(cols):
                text = self._game.read(x, y)
                self.write(text, (x, y))
        status = self._game.status()
        self.write(status, (0, rows), cols)
        
    def draw_nums_tents(self, cols, rows):
        # drawing num tents for the colums
        for x in range(rows):
            text = str(self._game.get_row_real_tents(x))
            pos = (x , -1)
            self.write(text, pos)

        # drawing num tents for the colums
        for y in range(cols):
            text = str(self._game.get_column_real_tents(y))
            pos = (-1 , y)
            self.write(text, pos)


    def write(self, text, pos, cols=1):
        x, y = pos        
        g2d.set_color(WHITE)
        g2d.draw_rect((x * W + 1 + DX, y * H + 1 + DY), (cols * W - 2, H - 2))
        
        last = text[-1:]
        if cols == 1 and last in self._annots:
            color, stroke = self._annots[last]
            g2d.set_color(color, stroke)
            g2d.draw_circle((x * W + W / 2 + DX, y * H + W / 2 + DY), min(W , H ) / 2 - 2)
            text = text[:-1]
        
        chars = max(1, len(text))
        fsize = min(0.75 * H, 1.5 * cols * W / chars)
        center = (x * W + cols * W/2 + DX, y * H + H/2 + DY)
        
        # section of choceing che 
        if text == "green":
            g2d.set_color(GREEN)
            g2d.draw_rect((x * W + 1 + DX, y * H + 1 + DY), (cols * W - 2, H - 2 ))
        elif text == "⛺" or text == "🌳":
            g2d.set_color(GREEN)
            g2d.draw_rect((x * W + 1 + DX, y * H + 1 + DY), (cols * W - 2 , H - 2))
            g2d.set_color(BLACK)
            g2d.draw_text(text, center, fsize)
        else:
            g2d.set_color(BLACK)
            g2d.draw_text(text, center, fsize)

def gui_play(game: BoardGame):
    g2d.init_canvas((game.cols() * W + DX, game.rows() * H + H + DY))
    ui = BoardGameGui(game)
    g2d.main_loop(ui.tick)

