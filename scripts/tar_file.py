# -*- coding: utf-8 -*-
import tarfile
import os
def tar(fname):
    file_list = os.listdir(fname)
    if len(file_list) == 0:
        print"There is no file to compress."
        return
    t = tarfile.open(fname + ".tar.gz", "w:gz")
    for root, dir, files in os.walk(fname):
        for file in files:
            fullpath = os.path.join(root, file)
            t.add(fullpath)
    t.close()

if __name__ == "__main__":
    tar("/home/dev/Data/Production/data4deepinews/html")