import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../src')
from score import *

def test_order():
    s1 = Score("Test1", 15)
    s2 = Score("Test1", 16)
    s3 = Score("Test2", 15)
    assert s1 == s3
    assert s1 != s2
    assert s1 < s2
    assert s1 <= s3
    assert s1 >= s3
