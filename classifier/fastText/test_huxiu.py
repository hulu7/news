# _*_coding:utf-8 _*_
import fasttext
import time
import csv
import fcntl
import jieba

base_dir = "/home/dev/Data/npl/classifier/fastText_huxiu/"
train_dir = base_dir + "train_data/"
test_dir = base_dir + "test_data/"
modle_dir = base_dir + "model_data/"
input_dir = test_dir + "input.csv"
output_dir = test_dir + "output.csv"

def readFromCSV(filePath):
    content = []
    with open(filePath, 'r') as scv_file:
        content = list(csv.reader(scv_file))
    scv_file.close()
    return content

def writeToCSVWithoutHeader(filePath, content):
    with open(filePath, 'a') as csv_file:
        fcntl.flock(csv_file.fileno(), fcntl.LOCK_EX)
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(content)
    csv_file.close()

print "start to load model..."
since = time.time()
classifier = fasttext.load_model(modle_dir + "news_fasttext.model.bin")
time_elapsed = time.time() - since
print('load model done in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))

texts = ['丰田 开放 专利 背后 ： 加快 行业 效率 ， 帮助 创新 企业 聚焦 创新 丨 汽车 预言家']
print "start to classify news..."
since = time.time()
all_contents = readFromCSV(input_dir)
all_contents.pop(0)
for item in all_contents:
    title = item[1]
    text = title.decode("utf-8").encode("utf-8")
    seg_text = jieba.cut(text.replace("\t", " ").replace("\n", " "))
    texts = [" ".join(seg_text)]
    labels = classifier.predict_proba(texts, k=1)
    print "title: {0} -- {1}".format(title, labels)
    if labels[0][0][0] == u'__label__Y':
        item.append('Y')
    else:
        item.append('N')
    writeToCSVWithoutHeader(output_dir, item)

time_elapsed = time.time() - since
print('Job done in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))