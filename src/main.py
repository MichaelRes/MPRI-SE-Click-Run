import sys
import pygame as pg
from state import *


def main():
    pg.init()
    screen = pg.display.set_mode((1200, 720))
    states = {
        "MAIN_MENU": state_main_menu.MainMenu(),
        "BEST_SCORE": state_best_score.BestScore(),
        "OPTIONS": state_options.Options(),
        "CREDITS": state_credits.Credits(),
        "GAME_OVER": state_game_over.GameOver(),
        "GAME": state_game_play.StateGamePlay(),
        "GAME_REPlAY": state_game_replay.StateGameReplay(),
        "PAUSE": state_pause.Pause(),
        "ADD_SCORE": state_add_score.AddScore(),
            }
    game = state_engine.Game(screen, states, "MAIN_MENU")
    game.run()
    pg.quit()
    sys.exit()


main()
