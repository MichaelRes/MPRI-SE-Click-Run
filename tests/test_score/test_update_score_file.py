import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../src')
from score import *

def test_update_score_file():
   sm = ScoreManager()
   s = Score("", 5)
   sm.instance.scores = [s]
   sm.update_score_file()
   with open(sm.instance.best_score_file, 'r') as f:
       l = [l for l in f]
       assert l[0] == ' 5\n'
   os.remove(sm.instance.best_score_file)
