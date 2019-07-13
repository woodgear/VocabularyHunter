import unittest
import json
from util import * 
class A:
    def __init__(self):
        self.a="a"
    def to_json_serializable(self):
        return self.__dict__

class Test(unittest.TestCase):
    def test_to_json(self):
        testcases = [
            ( {"a":"a"} , A() ),
            ( [{"a":"a"}] , [A()] ),
            ( {"a":{"a":"a"}} , {"a":A()} )
        ]
        for (left,right) in testcases:
            self.assertEqual(json.dumps(left),json.dumps(to_json_serializable(right)))
