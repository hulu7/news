# coding:utf-8

import codecs
import re
import json
import jieba
import jieba.posseg as posseg
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 我理解的加载dict.txt的作用： load_userdict可以正确的判断分词金常务而不会被切割成 金-常务 且盛京不会被判断成人名nr
# dict.txt的nr是词性【人名】的意思
# jieba.load_userdict('resource/dict.txt')
# 微信的文章说lineNames记录每一行出现的人名 我认为是个二维数组
lineNames = []
relationships = {}
# names{} 这里没有必要定义names对象 原文中names统计了所有人名出现的次数 对制作关系图没有帮助
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
split_list=re.split('。|！|\!|\.|？|\?', content)
sentence_list=list(filter(None, split_list))
for line in sentence_list:

    if (line == ''):
        break
    elif (line == '\r\n'):
        continue
    else:
        # print line
        wordArray = posseg.cut(line)

        # 每读一行就给lineNames加入一个数组
        lineNames.append([])
        for w in wordArray:
            if ((w.flag == 'nr' or
                 w.flag == 'n' or
                 w.flag == 'vn' or
                 w.flag == 'eng' or
                 w.flag == 'vn' or
                 w.flag == 'ns') and len(w.word) >= 2):
                lineNames[-1].append(w.word)

# 打印lineNames的结果
# for i in range(len(lineNames)):
# print '-'.join(lineNames[i])

for line in lineNames:
    # 双层for循环
    for name1 in line:
        for name2 in line:
            if name1 == name2:
                continue
            if relationships.get(name1) is None:
                relationships[name1] = {}

            if relationships[name1].get(name2) is None:
                relationships[name1][name2] = 1
            else:
                relationships[name1][name2] = relationships[name1][name2] + 1


# !!仔细看json.石宇.尚华=61
# !!仔细看json.石宇.秀安=81
# 原文中的这两个关系的次数也是61和81 说明大部分的统计是写对了
print json.dumps(relationships, ensure_ascii=False, encoding='UTF-8')
tojson = open('map.json', 'w')
tojson.write(json.dumps(relationships, ensure_ascii=False))
tojson.close()

file = open('map.json', 'r')
parent_object = json.load(file)
file.close()
all_layers = []
def find(parent_object, link_layer):
    for child_first_key in parent_object:
        if child_first_key == link_layer[len(link_layer) - 1]:
            child_object = parent_object[child_first_key]
            for child_second_key in child_object:
                if child_second_key not in link_layer:
                    link_layer.append(child_second_key)
                    return find(parent_object, link_layer)
    return link_layer

for child_first_key in parent_object:
    link_layer = [child_first_key]
    all_layers.append(find(parent_object, link_layer))

deep = []
for layer in all_layers:
    deep.append(len(layer))
deepest = str(max(deep))
file2 = open('result_json.txt', 'w')
file2.write(str(deepest))
file2.close()
print "deep: " + str(deepest)