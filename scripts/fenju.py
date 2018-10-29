#coding=utf-8

import re
import sys
import thulac
reload(sys)
sys.setdefaultencoding('utf-8')
import jieba
import jieba.posseg as pseg
import jieba.analyse

pos_file='pos_file.txt'
clean_file='clean_file.txt'
result_file='result_file.txt'
infile = open(pos_file,'r')
clean_file=open(clean_file, 'w')
for line in infile.readlines():
    line = line.strip('\r\n')
    clean_file.write(line)
clean_file.close()
infile.close()

clean_file='clean_file.txt'
file = open(clean_file,'r')
content = file.read()
file.close()

splt=re.split('。|！|\!|\.|？|\?', content)
result_file='result_file.txt'
file=open(result_file, 'w')
for p in splt:
    file.write(p.decode('utf-8') + '\n')
    words = pseg.cut(p)
    for word, flag in words:
        # w=re.split('[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+', word)
        file.write(word.decode('utf-8') + '---' + flag + '\n')
file.close()