import jieba
import os
import csv
import time
import pandas as pd

base_dir = "/home/dev/Data/npl/classifier/fastText_huxiu/"
source_dir = base_dir + "source_data/"
train_dir = base_dir + "train_data/"
test_dir = base_dir + "test_data/"
modle_dir = base_dir + "model_data/"
ctrain = 0.80;

ftrain = open(train_dir + "news_fasttext_train_huxiu.txt","w")
ftest = open(test_dir + "news_fasttext_test_huxiu.txt","w")

# source_files = [
#     train_dir + "/huxiu_train.csv",
#     train_dir + "/ifeng_train.csv"
# ]

source_files = [
    test_dir + "/huxiu_test.csv",
    test_dir + "/ifeng_test.csv"
]

def readFromCSV(filePath):
    content = []
    with open(filePath, 'r') as scv_file:
        content = list(csv.reader(scv_file))
    scv_file.close()
    return content

print('starting classify news...')
since = time.time()
for file in source_files:
    start = time.time()
    indir = file
    lines = readFromCSV(indir)
    lines.pop(0)
    for line in lines:
        title = line[0]
        text = title.decode("utf-8").encode("utf-8")
        seg_text = jieba.cut(text.replace("\t", " ").replace("\n", " "))
        outline = " ".join(seg_text)
        if indir == source_files[0]:
            outline = outline.encode("utf-8") + "\t__label__Y\n"
        else:
            outline = outline.encode("utf-8") + "\t__label__N\n"
        # ftrain.write(outline)
        # ftrain.flush()
        ftest.write(outline)
        ftest.flush()
        continue
    time_elapsed = time.time() - start
    print('process done for' + file + ' Complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))

ftrain.close()
ftest.close()
print "done!"
time_elapsed = time.time() - since
print('Complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))