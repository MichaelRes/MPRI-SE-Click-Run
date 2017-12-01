import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../src')
from map import *

def test_new_map():
    """
    This function gives an instance for the map class without going further
    """
    pg.init()
    screen = pg.display.set_mode((1200, 720))
    new_map = Map()
    pg.quit()
