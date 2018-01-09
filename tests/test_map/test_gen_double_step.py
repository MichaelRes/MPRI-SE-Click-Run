import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../src')
from map import *

def test_double_step():
    """
    This function try to generate the double step pattern
    """
    new_map = Map(None,None)
    for i in range(1000):
        new_map.gen_double_step()

