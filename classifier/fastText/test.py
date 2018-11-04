# _*_coding:utf-8 _*_
import fasttext
import time
base_dir = "/home/dev/Repository_Test_Data/classifier/fastText/"
train_dir = base_dir + "train_data/"
test_dir = base_dir + "test_data/"
modle_dir = base_dir + "model_data/"

print "start to load model..."
since = time.time()
classifier = fasttext.load_model(modle_dir + "news_fasttext.model.bin")
time_elapsed = time.time() - since
print('load model done in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))

texts = ['房']
print "start to classify news..."
since = time.time()
labels = classifier.predict_proba(texts, k=4)
print labels
time_elapsed = time.time() - since
print('Job done in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))