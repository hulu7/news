# -*- coding: utf-8 -*-
import jieba
import jieba.posseg as pseg
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import csv

input_path = '/home/dev/Fenci/huxiu/'
output_path = '/home/dev/Fenci/huxiu_fenci/'

for root, dirs, files in os.walk(input_path):
    for file in files:
        file_in = open(root + file, 'r')
        content = file_in.read()
        file_in.close()
        words = pseg.cut(content)
        file_out = open(output_path + file + '.csv', 'w')
        csv_write = csv.writer(file_out)
        fileHeader = ["word", "flag"]
        csv_write.writerow(fileHeader)
        for word, flag in words:
            csv_write.writerow([word , flag])
        file_out.close()
print ("write over")