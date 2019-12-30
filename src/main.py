# -*- coding: utf-8 -*-
import sys
import pygame as pg
sys.path.append('state')
from state_engine import *
from state_main_menu import *
from state_best_score import *
from state_options import *
from state_credits import *
from state_game_over import *
from state_game import *
from state_pause import *
from state_add_score import *

def main():
    pg.init()
    screen = pg.display.set_mode((1200, 720))
    states = {
        "MAIN_MENU": MainMenu(),
        "BEST_SCORE": BestScore(),
        "OPTIONS": Options(),
        "CREDITS": Credits(),
        "GAME_OVER": GameOver(),
        "GAME": StateGame(),
        "PAUSE": Pause(),
        "ADD_SCORE": AddScore(),
            }
    game = Game(screen, states, "MAIN_MENU")
    game.run()
    pg.quit()
    sys.exit()

main()

