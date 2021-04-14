import os

path = r"/home/zhao/mydata/data1/case1000/"
f = os.listdir(path)
for name in f:
    newname = name[0:-9] + ".png"
    os.rename(path+name,path+newname)