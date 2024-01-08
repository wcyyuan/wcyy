#!/usr/bin/python3
# 比较文件夹下面是否有相同的文件名

import os
import os.path
rootdir="/Users/anon/Development/GitHub/codwam.github.io/debfiles/" #要查找的目录

result = []
def findSame(parent,filenames,category):
    for filename in filenames:
        print(filename)
        for filename2 in filenames:
            if filename != filename2:
                if filename.lower() == filename2.lower():
                    message = category + parent + " / " + filename + "==" + filename2
                    if not message in result:
                        result.append(message)

print("start find...")
for parent,dirnames,filenames in os.walk(rootdir):
    # print("1. ", filenames)
    for dirname in dirnames:
        findSame(parent,dirnames,"find folder ")
        #print  "dirname is:  " + dirname

    #for filename in filenames:
        #print "parent is: " + parent
        #print "filename is: " + filename
    findSame(parent,filenames,"find file ")

print("done.\n")

if len(result) > 0:
    print("result is:")
    for message in result:
        print(message)
else:
    print("no same file or folder found.")