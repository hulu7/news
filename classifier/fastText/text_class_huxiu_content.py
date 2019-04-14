import jieba
import os
import csv
import time
import pandas as pd

base_dir = "/home/dev/Data/npl/classifier/fastText_huxiu_content/"
source_dir = "{0}source_data/".format(base_dir)
train_dir = "{0}train_data/".format(base_dir)
test_dir = "{0}test_data/".format(base_dir)
modle_dir = "{0}model_data/".format(base_dir)
raw_dir = "{0}raw_data/".format(base_dir)
ctrain = 0.80

ftrain = open("{0}news_fasttext_train_huxiu_content.txt".format(train_dir), "w")
# ftest = open("{0}news_fasttext_test_huxiu_content.txt".format(test_dir), "w")

source_files = [
     "{0}huxiu_washed/".format(raw_dir),
     "{0}ifeng_washed/".format(raw_dir)
]

# source_files = [
#      "{0}huxiu_washed_test/".format(raw_dir),
#      "{0}ifeng_washed_test/".format(raw_dir)
# ]

def readFromCSV(filePath):
    content = []
    with open(filePath, 'r') as scv_file:
        content = list(csv.reader(scv_file))
    scv_file.close()
    return content

def readFromTxt(file_path):
    with open(file_path, 'r') as txt_file:
        content = txt_file.read()
    txt_file.close()
    return content

print('starting classify news...')
since = time.time()
for source in source_files:
    files = os.listdir(source)
    for file in files:
        print "processing file: {0}".format(file)
        file_path = "{0}{1}".format(source, file)
        text = readFromTxt(file_path)
        text_decode = text.decode("utf-8").encode("utf-8")
        seg_text = jieba.cut(text_decode.replace("\t", " ").replace("\n", " "))
        outline = " ".join(seg_text)
        if source == source_files[0]:
            outline = outline.encode("utf-8") + "\t__label__Y\n"
        else:
            outline = outline.encode("utf-8") + "\t__label__N\n"
        ftrain.write(outline)
        ftrain.flush()
        # ftest.write(outline)
        # ftest.flush()
        continue
    time_elapsed = time.time() - since
    print('process done for' + file + ' Complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))

ftrain.close()
# ftest.close()
print "done!"
time_elapsed = time.time() - since
print('Complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))