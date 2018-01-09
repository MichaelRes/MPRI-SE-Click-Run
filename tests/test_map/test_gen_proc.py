import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../src')
from map import *

def test_gen_proc():
    """
    This function try to generate the map
    """
    new_map = Map(None)
    for i in range(1000):
        new_map.gen_proc()

