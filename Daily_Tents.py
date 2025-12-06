import boardgame
from random import shuffle
import copy
from time import sleep

#   little rappresentation of the cells around
POSITIONS_CELLS_AROUND = [
    (-1, -1),(0, -1),(1, -1),
    (-1, 0),          (1,  0),
    (-1, +1),(0, +1),(+1,+1)
]

POSITIONS_CELLS_ADJACENT = [
            (0, -1),
    (-1, 0),          (1,  0),
            (0, +1)
]

class Daily_Tents(boardgame.BoardGame):
    def __init__(self, file: str):
        super().__init__()
        self._w, self._h = 0,0
        self._col_t = []
        self._row_t = []
        self._board = self.initialize_board_file(file)
        self._real_board = copy.deepcopy(self._board)

    def play(self, x, y, action):
        if action == "automate_green":
            self.automate_green()
        if action == "automate_tents":
            self.automate_tents()
        if action == "automatism":
            self.automatism()
        if 0 <= x < self.cols() and 0 <= y < self.rows():
            if self.read(x, y) == "":
                self.add_green((x, y))
            elif self.read(x, y) == "green":
                if self.count_tents()+1 <= self.count_tree():
                    self.add_tent((x, y))
            elif self.read(x, y) == "⛺":
                self.clear_cell((x, y))
            
    def initialize_board_file(self, file: str):
        dic = {
            ".":"",
            "T":"🌳"
        }
        board = []
        with open(f"{file}", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f]
        self._row_t = [int(c) for c in lines[0][1:]]
        for line in lines[1:]:
            self._col_t.append(int(line[0]))
            board.append([dic[c] for c in line[1:]])

        self._h = len(board)
        self._w = len(board[0])
        return board
    
    def remove_tents(self):
        for y in range(self.rows()):
            for x in range(self.cols()):
                if self.is_tent((x, y)):
                    self.clear_cell((x, y))
                

    def initialize_tents(self, positions):
        for p in positions:
            self.add_tent(p)

    def automatism(self):
        self.try_out_all_opts()

    def try_out_all_opts(self):
        for y in range(self.rows()):
            for x in range(self.cols()):
                if self.read(x, y) == "":
                    self.try_out_opts(x, y)

    def try_out_opts(self, x, y):
        copy1 = copy.deepcopy(self)
        copy1.play(x, y, "")  # play option 1
        copy1.automate_green()
        copy1.automate_tents()
        copy2 = copy.deepcopy(self)
        copy2.play(x, y, "")  # play option 2
        copy2.play(x, y, "")
        copy2.automate_green()
        copy2.automate_tents()
        
        if copy1.wrong():
            self.play(x, y, "")  # play option 2
            self.play(x, y, "")
        elif copy2.wrong():
            self.play(x, y, "")  # play option 1
        else:
            # find unavoidable outcome in some other cell @ (xo, yo)
            for yo in range(self.rows()):
                for xo in range(self.cols()):
                    if (self.read(xo, yo) == "" and
                        copy1.read(xo, yo) == copy2.read(xo, yo) != ""):
                        if copy1.read(xo, yo) == "⛺":
                            self.play(xo, yo, "")
                            self.play(xo, yo, "")
                        else:
                            self.play(xo, yo, "")

    def automate_green(self):
        for y in range(self.rows()):
            for x in range(self.cols()):
                if self.read(x, y) == "" and self.check_around((x, y), "🌳") == 0:
                    self.add_green((x, y))

    def automate_tents(self):
        for x, y in self.get_tree_pos():
            for dx, dy in POSITIONS_CELLS_AROUND:
                if 0 <= x+dx < self.cols() and 0 <= y+dy < self.rows():
                    new_x = x+dx
                    new_y = y+dy
                    num_tr = self.get_row_tents(new_x)
                    num_tc = self.get_column_tents(new_y)
                    if (num_tr+1<=self.get_row_real_tents(new_x) and
                        num_tc+1<=self.get_column_real_tents(new_y) and
                        self.check_around((new_x, new_y), "⛺") == 0 and
                        #comment the line below to win instantly
                        self.read(new_x, new_y) != "green"):
                        self.add_tent((new_x, new_y))

    def initialize_tree(self, positions):
        for p in positions:
            self.add_tree(p)

    def clear_cell(self, pos):
        x, y = pos
        self._board[y][x] = ""

    def is_tent(self, pos):
        x, y = pos
        if self.read(x, y) == "⛺":
            return True
        return False
    
    def add_green(self, pos):
        x, y = pos
        self._board[y][x] = "green"
    
    def add_tree(self, pos):
        x, y = pos
        self._board[y][x] = "🌳"

    def add_tent(self, pos):
        x, y = pos
        if self.read(x, y) != "🌳":
            self._board[y][x] = "⛺"

    def board(self): return self._board

    def read(self, x, y): 
        return str(self._board[y][x])
    
    def get_column_real_tents(self, y) -> int:
        return self._col_t[y]
    
    def get_row_real_tents(self, x):
        return self._row_t[x]
    
    def get_column_tents(self, y) -> int:
        num = 0
        for x in range(self.cols()):
            if self.is_tent((x, y)):
                num += 1
        return num
    
    def get_row_tents(self, x):
        num = 0
        for y in range(self.rows()):
            if self.is_tent((x, y)):
                num += 1
        return num
        

    def count_tree(self):
        num_tents = 0
        for row in self._board:
            for cell in row:
                if cell == "🌳": num_tents += 1
        return num_tents

    def count_tents(self):
        num_tents = 0
        for row in self._board:
            for cell in row:
                if cell == "⛺": num_tents += 1
        return num_tents
                    
    def get_tree_pos(self) -> list[tuple[int, int]]:
        positions = []
        for y,row in enumerate(self._board):
            for x, cell in enumerate(row):
                if cell == "🌳": positions.append((x, y))
        return positions
    
    def get_tents_pos(self) -> list[tuple[int, int]]:
        positions = []
        for y,row in enumerate(self._board):
            for x, cell in enumerate(row):
                if cell == "⛺": positions.append((x, y))
        return positions
    
    def wrong(self) -> bool:
        control = False
        control = control or any(self.get_column_tents(x) > self.get_column_real_tents(x) for x in range(self.cols()))
        control = control or any(self.get_row_tents(y) > self.get_row_real_tents(y) for y in range(self.rows()))
        control = control or any(self.check_around(pos, "green")==self.count_cell_around(pos) and self.check_around(pos, "⛺")==0 
                                 for pos in self.get_tree_pos())
        control = control or any(self.check_around(pos, "⛺") > 0 for pos in self.get_tents_pos())
        return control


    def check_around(self, pos, element):
        n=0
        for dx, dy in POSITIONS_CELLS_AROUND:
            x, y = pos
            x, y = x+dx, y+dy
            if 0 <= x < self.cols() and 0 <= y < self.rows():
                if self.read(x, y) == element:
                    n+=1
        return n
    
    def count_cell_around(self, pos):
        n=0
        for dx, dy in POSITIONS_CELLS_AROUND:
            x, y = pos
            x, y = x+dx, y+dy
            if 0 <= x < self.cols() and 0 <= y < self.rows():
                n+=1
        return n
    
    def check_adjacent(self, pos, element):
        #"⛺""🌳"
        n=0
        for dx, dy in POSITIONS_CELLS_ADJACENT:
            x, y = pos
            x, y = x+dx, y+dy
            if 0 <= x < self.cols() and 0 <= y < self.rows():
                if self.read(x, y) == element:
                    n+=1
        return n  

    def constraint(self):
        # row check
        control = not any(self.get_column_real_tents(x) != self.get_column_tents(x) for x in range(self.cols()))
        # cols check
        control = control and not any(self.get_row_real_tents(y) != self.get_row_tents(y) for y in range(self.rows()))
        # check around
        control = control and not any(self.check_around(t_p, "⛺") != 0 for t_p in self.get_tents_pos())
        return control


    def finished(self):
        control = self.count_tents() == self.count_tree()
        #print(f"check 1: {control}")
        control = control and not any(self.check_around(x, "⛺") == 0 for x in self.get_tree_pos())
        #print(f"check 2: {control}")
        control = control and not any(self.check_around(x, "🌳") == 0 for x in self.get_tents_pos())
        #print(f"check 3: {control}")
        control = control and self.constraint()
        return control

    def rows(self): return self._h
    
    def cols(self): return self._w

    def status(self):
        return "Partita conclusa!" if self.finished() else "Gioca..."
    
    def print_board(self):
        for x in self._board:
            print("\t".join(cell if cell!="" else "." for cell in  x))

def main():
    b = Daily_Tents("tents-games/tents-2025-11-27-8x8-easy.txt")
    # boardgame.print_game(b)

if __name__ == "__main__":
    main()