import jieba
import os
import csv
import time

base_dir = "/home/dev/Repository_Test_Data/classifier/fastText/"
source_dir = base_dir + "source_data/"
train_dir = base_dir + "train_data/"
test_dir = base_dir + "test_data/"
modle_dir = base_dir + "model_data/"
ctrain = 0.80;

ftrain = open(train_dir + "news_fasttext_train.txt","w")
ftest = open(test_dir + "news_fasttext_test.txt","w")

classes = {}
source_files = os.listdir(source_dir)

print('starting count...')
since = time.time()
for file in source_files:
    indir = source_dir + file
    with open(indir, 'r') as fr:
        lines = fr.readlines()
    for line in lines:
        extract_items = line.split('_!_')
        if len(extract_items) < 4:
            continue
        catalog_items = extract_items[2].split('_')
        if len(catalog_items) > 1:
            catalog = catalog_items[1]
        else:
            catalog = catalog_items[0]
        if classes.get(catalog) is None:
            classes[catalog] = {}
        if classes[catalog].get('count') is None:
            classes[catalog]['count'] = 1
        else:
            classes[catalog]['count'] += 1
    fr.close()

for item in classes:
    with open(modle_dir + "classes.csv", 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([item, classes[item]['count']])
    csv_file.close()
time_elapsed = time.time() - since
print('count done for' + file + ' Complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))

train_test_data_split = {}

print('starting classify news...')
for file in source_files:
    start = time.time()
    indir = source_dir + file
    with open(indir, 'r') as fr:
        lines = fr.readlines()
    for line in lines:
        extract_items = line.split('_!_')
        if len(extract_items) < 4:
            continue
        catalog_items = extract_items[2].split('_')
        if len(catalog_items) > 1:
            catalog = catalog_items[1]
        else:
            catalog = catalog_items[0]
        if catalog in ['', 'all', 'local', 'news', 'essay', 'world', 'article', 'media'] or classes[catalog]['count'] < 1000:
            continue
        if train_test_data_split.get(catalog) is None:
            train_test_data_split[catalog] = {}
        if train_test_data_split[catalog].get('count') is None:
            train_test_data_split[catalog]['count'] = 1
        else:
            train_test_data_split[catalog]['count'] += 1

        keywords_items = extract_items[4].split(',')
        title = extract_items[3]
        keywords = extract_items[4]
        content = title + ',' + keywords

        text = title.decode("utf-8").encode("utf-8")
        seg_text = jieba.cut(text.replace("\t", " ").replace("\n", " "))
        outline = " ".join(seg_text)
        outline = outline.encode("utf-8") + "\t__label__" + catalog + "\n"
        if train_test_data_split[catalog]['count'] < classes[catalog]['count'] * ctrain:
            ftrain.write(outline)
            ftrain.flush()
            continue
        else:
            ftest.write(outline)
            ftest.flush()
            continue
    fr.close()
    time_elapsed = time.time() - start
    print('process done for' + file + ' Complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))

ftrain.close()
ftest.close()
print "done!"
time_elapsed = time.time() - since
print('Complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))