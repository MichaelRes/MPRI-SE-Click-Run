import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../src')
from score import *

def test_pos_as_score_and_add_score():
    sm = ScoreManager()
    sm.instance.scores = []
    print(sm.instance.scores)
    for i in range(sm.max_number_of_score):
        s = Score("", i*2)
        p = sm.pos_as_score(s)
        assert p == 0
        sm.add_score(s, p)
    for i in range(sm.max_number_of_score-1):
        assert sm.instance.scores[i].score >= sm.instance.scores[i].score
    for i in range(sm.max_number_of_score):
        s = Score("", i*2 + 1)
        p = sm.pos_as_score(s)
        assert p == sm.max_number_of_score - 1 - i
    os.remove(sm.instance.best_score_file)

