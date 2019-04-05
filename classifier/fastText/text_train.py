# _*_coding:utf-8 _*_
import fasttext
import time
base_dir = "/home/dev/Data/npl/classifier/fastText_huxiu/"
train_dir = base_dir + "train_data/"
test_dir = base_dir + "test_data/"
modle_dir = base_dir + "model_data/"
#训练模型
print "start training..."
since = time.time()
classifier = fasttext.supervised(train_dir + "news_fasttext_train_huxiu.txt", modle_dir + "news_fasttext.model",label_prefix="__label__")
time_elapsed = time.time() - since
print('training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))

result = classifier.test(test_dir + "news_fasttext_test_huxiu.txt")
print result.precision
print result.recall

texts = ['呼和浩特 一 小区 居民楼 爆炸   已致 1 死 2 伤']

labels = classifier.predict_proba(texts, k=1)
print labels