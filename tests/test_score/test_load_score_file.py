import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../src')
from score import *

def test_load_score_file():
    sm = ScoreManager()
    sm.instance.scores = []
    s = [Score("a", sm.max_number_of_score -1 -i) for i in range(sm.max_number_of_score)]
    with open(sm.instance.best_score_file, 'w') as f:
        for e in s:
            f.write(str(e))
    sm.instance.scores = sm.instance.load_score_file()
    assert len(s) == len(sm.instance.scores)
    for i in range(len(s)):
        assert sm.instance.scores[i].pseudo == s[i].pseudo
        assert sm.instance.scores[i].score == s[i].score
    #os.remove(sm.instance.best_score_file)
