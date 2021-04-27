import os
import pandas as pd

scale = 400
output = False
mask_threshold = 0.5
channels = 1

##检测用的模型
model = './checkpoints/CP_epoch1000.pth'

##是否保存图片
no_save = False

##是否可视化结果
viz = False

##要检测的图像
# df=pd.read_csv('/home/zhao/mydata/to/ddsm.csv')
# list=[]
# for i in range(32):
#     list.append('/home/zhao/mydata/to/'+df['path'][i])
#
# pre_img = list
pre_img=['/home/zhao/mydata/ddsm3/DDSM_PNG/cancers/cancer_03/case1086/A_1086_1.LEFT_CC.png']
