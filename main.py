from Daily_Tents import Daily_Tents
import boardgame
import boardgameGui

def main():
    game = Daily_Tents(5, 5)
    # boardgame.console_play(game)
    # gui = boardgameGui(game)
    boardgameGui.gui_play(game)


if __name__ == "__main__":
    main()

