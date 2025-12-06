import unittest
from unittest.mock import Mock
from Daily_Tents import Daily_Tents
class Test_Daily_Tents(unittest.TestCase):
    # python -m unittest Test_Daily_Tents.py
    def test_play(self):
        game = Daily_Tents("tents-games/tents-2025-11-27-8x8-easy.txt")
        game.play(0, 0, "")
        state = game.read(0,0)
        self.assertEqual(state, 'green')
    
    def test_finished(self):
        game = Daily_Tents("tents-games/tents-2025-11-27-8x8-easy.txt")
        solution1 = [(2, 1), (5, 1),(7, 1),(0, 2),(3, 3),(7, 3),(5, 4),(0, 5),(2, 5),(7, 5),(4, 6),(1, 7)]
        for pos in solution1:
            x, y = pos
            game.play(x,y,"")
            game.play(x,y,"")
        self.assertEqual(game.finished(), True)

        game = Daily_Tents("tents-games/tents-2025-11-27-8x8-easy.txt")
        solution2 = [(1, 1), (3, 1), (7, 1), (5, 2), (0, 3), (7, 3), (2, 4), (0, 5), (4, 5), (7, 5), (2, 6), (5, 7)]
        for pos in solution1:
            x, y = pos
            game.play(x,y,"")
            game.play(x,y,"")
        self.assertEqual(game.finished(), True)



if __name__ == "__main__": 
    unittest.main()
