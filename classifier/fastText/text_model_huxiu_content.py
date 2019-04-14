# coding:utf-8

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import numpy as np
from gensim import corpora, models, similarities
from pprint import pprint
import time
import jieba
import os
from six import iteritems
import csv

base_dir = "/home/dev/Data/npl/classifier/fastText_huxiu_content/"
source_dir = "{0}source_data/".format(base_dir)
train_dir = "{0}train_data/".format(base_dir)
test_dir = "{0}test_data/".format(base_dir)
modle_dir = "{0}model_data/".format(base_dir)
raw_dir = "{0}raw_data/".format(base_dir)

fw = open("{0}news.tab".format(modle_dir),"w") #保存切分好的文本数据
fw_type = open("{0}type.tab".format(modle_dir),"w") #保存新闻类型，与news.tab一一对应
num = -1
source_files = [
    "{0}huxiu_washed/".format(raw_dir),
    "{0}ifeng_washed/".format(raw_dir)
]

train_test_data_split = {}

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

print "starting..."
since = time.time()

for source in source_files:
    files = os.listdir(source)
    for file in files:
        print "processing file: {0}".format(file)
        file_path = "{0}{1}".format(source, file)
        text = readFromTxt(file_path)
        text_decode = text.decode("utf-8").encode("utf-8")
        seg_text = jieba.cut(text_decode.replace("\t", " ").replace("\n", " "))
        outline = " ".join(seg_text) + "\n"
        outline = outline.encode("utf-8")
        fw.write(outline)
        fw.flush()
        fw_type.write(str(num) + "\n")
        fw_type.flush()
print "read file done!"
fw.close()
fw_type.flush()

def load_stopwords():
    f_stop = open('{0}stopwords.tab'.format(modle_dir))
    sw = [line.strip().decode("utf-8") for line in f_stop]
    f_stop.close()
    return sw
stop_words = load_stopwords()

print 'build dictionary--'
t_start = time.time()
dictionary = corpora.Dictionary(line.split() for line in open('{0}news.tab'.format(modle_dir)))
stop_ids = [dictionary.token2id[stopword] for stopword in stop_words if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid,docfreq in iteritems(dictionary.dfs) if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)
dictionary.compactify()
dictionary.save('{0}corpora.dict'.format(modle_dir))
print "build dictionary done，takes %.3f s" % (time.time() - t_start)

#dictionary = corpora.Dictionary.load('corpora.dict') #使用保存的dictionary


print "start to calculate the text vector --"
t_start = time.time()
class MyCorpus(object):
    def __iter__(self):
        for line in open("{0}news.tab".format(modle_dir)):
            yield dictionary.doc2bow(line.split())
corpus_memory_friendly = MyCorpus()
corpus = []
for vector in corpus_memory_friendly:
    corpus.append(vector)
print "text vector done，takes %.3f s" % (time.time() - t_start)

print 'start to save text vector--'
t_start = time.time()
corpora.MmCorpus.serialize("{0}corpus.mm".format(modle_dir),corpus) #保存生成的corpus向量
print "save text vector done，takes%.3f s" % (time.time() - t_start)

corpus = corpora.MmCorpus(modle_dir + "./corpus.mm") #使用保存的corpus向量

print "done!"
time_elapsed = time.time() - since
print('Complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))