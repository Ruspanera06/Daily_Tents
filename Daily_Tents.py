import boardgame

#   little rappresentation of the cells around
# POSITIONS_CELLS_AROUND = [
#     (-1, -1),(0, -1),(1, -1),
#     (1, 0),          (1,  0),
#     (-1, +1),(0, +1),(+1,+1)
# ]

POSITIONS_CELLS_AROUND = [
            (0, -1),
    (-1, 0),          (1,  0),
            (0, +1)
]

class Daily_Tents(boardgame.BoardGame):
    def __init__(self, w, h):
        super().__init__()
        self._w, self._h = w, h
        self._board = self.initializa_board(self._w, self._h)
        self._finished = False
        #comment the section below when the test is finished
        #______________________________________________
        postions_tree = [
            (1, 0),
            (4, 1),
            (1, 2),
            (3, 2),
            (4, 3),
        ]
        self.initialize_tree(postions_tree)
        #______________________________________________

    def play(self, x, y, action):
        self.add_tent((x, y))
    
    def initializa_board(self, w, h) -> list[list]:
        # width wich means the amount of cols we will have
        # heigth wich means the amount of rows we will have
        #The matrix will have [x(for the cols)][y(for the row)]
        board = []
        for i in range(h):
            tmp = []
            for j in range(w):
                tmp.append("")
            board.append(tmp)
        return board
    
    def add_tree(self, pos):
        x, y = pos
        self._board[y][x] = "🌳"

    def initialize_tree(self, positions):
        for p in positions:
            self.add_tree(p)

    def add_tent(self, pos):
        x, y = pos
        if self.read(x, y) != "🌳":
            self._board[y][x] = "⛺"

    def board(self): return self._board

    def read(self, x, y): 
        return str(self._board[y][x])

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
    
    def check_tents_around(self, pos):
        for dx, dy in POSITIONS_CELLS_AROUND:
            x, y = pos
            x, y = x+dx, y+dy
            if 0 <= x < self.cols() and 0 <= y < self.rows():
                if self.read(x, y) == "⛺":
                    return 1
        return 0
    
    def check_tree_around(self, pos):
        for dx, dy in POSITIONS_CELLS_AROUND:
            x, y = pos
            x, y = x+dx, y+dy
            if 0 <= x < self.cols() and 0 <= y < self.rows():
                if self.read(x, y) == "🌳":
                    return 1
        return 0

    def finished(self): 
        count_tree = 0
        count_tents = 0
        for pos in self.get_tree_pos():
            count_tree += self.check_tents_around(pos)
        for pos in self.get_tents_pos():
            count_tents += self.check_tree_around(pos)
        return count_tents == count_tree and self.count_tree() == self.count_tents()

    def rows(self): return self._h
    
    def cols(self): return self._w

    def status(self):
        return "Partita conclusa!" if self.finished() else "Gioca..."
    
    def print_board(self):
        for x in self._board:
            print("\t".join(cell if cell!="" else "." for cell in  x))

def main():
    b = Daily_Tents(5, 5)
    # b.print_board()
    # print(b.read(1, 0))
    boardgame.print_game(b)

if __name__ == "__main__":
    main()