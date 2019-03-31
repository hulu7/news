# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import struct

class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter(object):
    def __init__(self, server, key, blockNum=1):
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31]
        # self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.server = server
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def isContains(self, str_input):
        if not str_input:
            return False
        ret = True

        name = self.key + str(struct.unpack("h", str_input[0:2])[0] % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return ret

    def insert(self, str_input):
        name = self.key + str(struct.unpack("h", str_input[0:2])[0] % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)

if __name__ == '__main__':
    import redis
    text = u'要安全，不要自拍 俄将禁止执勤军人用智能手机'
    rconn = redis.Redis('127.0.0.1', 6379)
    bf = BloomFilter(rconn, 'test:dupefilter')
    if bf.isContains(text.encode("utf-8")):
        print 'exist!'
    else:
        bf.insert(text.encode("utf-8"))
        print 'not exist!'