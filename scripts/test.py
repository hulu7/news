# -*- coding: utf-8 -*-

class Test():

    def __init__(self):
        self.a = {
            "test":'1',
            "test1": 'c'
        }

    def test(self):
        b = self.a
        c = 1


if __name__ == '__main__':
    test=Test()
    test.test()