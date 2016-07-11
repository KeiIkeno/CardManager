
# coding: utf-8

# # 遊戯王カードリスト作成ツール
#     
#     使用方法：予めカードのイメージをスキャンし、imageフォルダに配置する。

# In[625]:

import os
import time
IMAGE_PATH = './image'
ID_PATH = './id'
IDTXT_PATH = './idtxt'
CUT_PIX = '47+1930'


# In[626]:

os.system('rm -rf {0}'.format(ID_PATH))
os.system('rm -rf {0}'.format(IDTXT_PATH))
os.system('mkdir {0}'.format(IMAGE_PATH))
os.system('mkdir {0}'.format(ID_PATH))
os.system('mkdir {0}'.format(IDTXT_PATH))


# In[627]:

images = os.listdir(IMAGE_PATH)


# In[628]:

images.sort()


# In[630]:

for image in images:
    os.system('convert -crop 16%x2.8%+{3} -modulate 105 "{0}/{1}" "{2}/id_{1}"'.format(IMAGE_PATH, image, ID_PATH, CUT_PIX))
#    os.system('convert -noise 1 -threshold 17700 "{0}/id_{1}" "{0}/monoid_{1}"'.format(ID_PATH, image))
#    os.system('convert -noise 3 "{0}/id_{1}" "{0}/monoid_{1}"'.format(ID_PATH, image))
    os.system('convert -level 0%,100%,2% -trim -fuzz 26% "{0}/id_{1}" "{0}/monoid_{1}"'.format(ID_PATH, image))
    os.system('rm -f "{0}/id_{1}"'.format(ID_PATH, image))


# In[631]:

ids = os.listdir(ID_PATH)


# In[632]:

for id in ids:
    os.system('tesseract "{0}/{1}" "{2}/{1}" -psm 7 tesseract.conf'.format(ID_PATH, id, IDTXT_PATH))


# In[633]:

idtxts = os.listdir(IDTXT_PATH)


# In[634]:

for idtxt in idtxts:
    os.system('tr -d " " < "{0}/{1}" >> "{0}/idlist.txt"'.format(IDTXT_PATH, idtxt, IDTXT_PATH))


# In[914]:

import pandas as pd
import numpy as np


# In[915]:

df = pd.read_csv('{0}/idlist.txt'.format(IDTXT_PATH), header=None, names=['パスワード'], dtype={'パスワード': np.str})


# In[916]:

df['枚数'] = 1


# In[917]:

df = df.groupby('パスワード').sum()


# In[918]:

cardlist = pd.read_csv('cardlist.csv', dtype={'パスワード': np.str})


# In[919]:

cardlist = cardlist.drop('Unnamed: 0', axis=1)


# In[920]:

cardlist = cardlist.set_index('パスワード')


# In[921]:

df = df.join(cardlist)


# In[923]:

df.to_csv('my_cardlist.csv')


# In[928]:

os.system('nkf -wsc --overwrite my_cardlist.csv')


# In[ ]:



