class Tents:
    def __init__(self):

        #   little rappresentation of the cells around
        positions = [
            (-1, -1),(0, -1),(1, -1),
            (1, 0),          (1,  0),
            (-1, +1),(0, +1),(+1,+1)
        ]
