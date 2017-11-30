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
    pg.init()
    screen = pg.display.set_mode((1200, 720))
    for i in range(100):
        new_map = Map(i)
        frequency = [0 for i in range(10)]
        for j in range(350): # With 350, the probability that the test give a illegitimate error should be inferior to 10^-10.
            frequency[new_map.randint(10)-1]+=1
        for j in range(10):
            assert frequency[j] != 0,"There's problem with random generation of the map for seed " + str(i)
        print(frequency)
    pg.quit()

