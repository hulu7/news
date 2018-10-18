import csv
csv_list = list(csv.reader(open("/home/dev/Desktop/ifeng.contentInfo.csv")))
url = []
cnt = []
total = 0
for f in range(len(csv_list)):
    url.append(csv_list[f][2])
    c = 0
    for e in range(f + 1, len(csv_list)):
        if csv_list[f][2] == csv_list[e][2]:
            csv_list.remove(csv_list[e])
            c += 1
            total += 1
    cnt.append(c)

for j in range(len(url)):
    if cnt[j] != 0:
        print str(url[j]) + " --- " + str(cnt[j])

print "total duplicate --- " + str(total)