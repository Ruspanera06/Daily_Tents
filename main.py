from Daily_Tents import Daily_Tents
import boardgame
import boardgameGui

def main():
    game = Daily_Tents("tents-games/tents-2025-11-27-8x8-easy.txt")
    boardgameGui.gui_play(game)


if __name__ == "__main__":
    main()

