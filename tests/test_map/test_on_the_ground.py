import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../src')
from map import *


def test_on_the_ground():
    pg.init()
    screen = pg.display.set_mode((1200, 720))
    new_map = Map()
    assert (not new_map.on_the_ground(0,0,(new_map.dim_bloc, new_map.dim_bloc)))
    assert (new_map.on_the_ground(0, new_map.dim_bloc * (new_map.height - 2) -1, (new_map.dim_bloc, new_map.dim_bloc)))
    assert (not new_map.on_the_ground(0, new_map.dim_bloc * (new_map.height - 2) -2, (new_map.dim_bloc, new_map.dim_bloc)))
    pg.quit()
