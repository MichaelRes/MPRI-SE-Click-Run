import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../src')
from map import *

def test_new_map():
    """
    This function should test that the randomness provided by the randint fuction of map
    should not be absurd for some seed.
    """
    for i in range(10):
        map1 = Map(None,i*1000)
        map2 = Map(None,i*1000)
        for j in range(100):
            map1.gen_one()
            map2.gen_one()
        for k in range(len(map1.data)):
            for l in range(len(map1.data[0])):
                assert map1.data[k][l] == map2.data[k][l], "Same seed should get same map"

