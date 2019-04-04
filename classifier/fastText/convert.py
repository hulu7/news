# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import time
import re
import csv

base_dir = "/home/dev/Data/npl/classifier/fastText_huxiu/"
source_dir = base_dir + "source_data/"
train_dir = base_dir + "train_data/"
test_dir = base_dir + "test_data/"
modle_dir = base_dir + "model_data/"
raw_dir = base_dir + "raw_data/"

classes = {}
raw_files = os.listdir(raw_dir)
#'1011429170|,|news_tech/internet,news_tech|,|【移动互联网新闻】百度搞钱包，移动支付打法又变了？|,|bat,互联网公司,百度,财付通,阿里,互联网,电商,支付宝,手机,移动端,移动互联网,支付'
print('starting...')
since = time.time()
for file in raw_files:
    indir = raw_dir + file
    converted_file = open(source_dir + file, "w")
    with open(indir, 'r') as fr:
        lines = fr.readlines()
    fr.close()
    for line in lines:
        extract_items = line.split('|,|')
        if len(extract_items) > 3:
            id = extract_items[0]
            catalog_items = re.split('[,/]', extract_items[1])
            if len(catalog_items) > 0:
                catalog = catalog_items[0]
            else:
                catalog = ''
            title = extract_items[2]
            if len(extract_items[3]) > 0:
                keywords = extract_items[3]
            else:
                keywords = ''
            new_line = id + '_!_' + '000' + '_!_' + catalog + '_!_' + title + '_!_' + keywords + '\n'
            converted_file.write(new_line)
            if classes.get(catalog) is None:
                classes[catalog] = {}
            if classes[catalog].get('count') is None:
                classes[catalog]['count'] = 1
            else:
                classes[catalog]['count'] += 1
    converted_file.close()

for item in classes:
    with open(raw_dir + "classes.csv", 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([item, classes[item]['count']])
    csv_file.close()
print "done!"
time_elapsed = time.time() - since
print('Complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))