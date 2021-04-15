import pandas as pd
from shutil import copy

path = '/home/zhao/mydata/ddsm3/DDSM_PNG.csv'
df = pd.read_csv(path)
for i in range(100):
    copy('/home/zhao/mydata/'+df['filepath'][i+454][3:], '/home/zhao/mydata/test/')
