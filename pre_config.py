import os

scale = 0.05
output = False
mask_threshold = 0.9
channels = 1

##检测用的模型
model = './checkpoints/CP_epoch200.pth'

##是否保存图片
no_save = False

##是否可视化结果
viz = False

##要检测的图像
list = os.listdir('/home/zhao/mydata/test')
for i in range(len(list)):
    list[i] = '/home/zhao/mydata/test/' + list[i]

pre_img = list
