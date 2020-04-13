#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc


# In[2]:


gd=pd.read_excel('ist_geri_kazanim_verisi.xlsx', 'Geri Kazanım Verisi', index_col="Geri Kazanım Verisi", columns=['Yıllar'], na_values=['NA'])
gd


# Bir çöp gazı yakma tesisinde ortalama net elektrik eldesi : 1.100 kWh /ton atık'dır.
#Kaynak: ÜNAL Enver, "Katı Atıktan Enerji Üretimi", HITACHI ZOSEN INOVA AG Hardturmstrasse 127, P.O.Box 680,CH-8037 Zurich, http://www.emo.org.tr/ekler/9d577b8f7ee7662_ek.pdf

# In[3]:


gd.iloc[3:4,::] = gd.iloc[3:4,::].apply(lambda x: 10*x/11)
gd1 = gd.rename(index={'Çöp Gazından Üretilen Elektrik Enerjisi Miktarları [MWh]': 'Çöp Gazından Elektrik Üretiminde Kullanılan Atık Miktarı[ton]'})


# In[4]:


gd1


# Atıktan yakıt türetme tesisine gelen 300 ton atıktan ortalama 81 ton plastik bazlı yakıt elde edilebilmektedir. 
#Kaynak1: İSTAÇ Stratejik Planı (2013-2017), İstanbul Çevre Yönetimi San. Ve Tic. A.Ş., http://istac.ssplab.com/contents/15/%C4%B0stac_Str_Plan%202(2).pdf. Erişim Tarihi: 28.10.2018.
#Kaynak2: ÇELİK Suna Özden, "Atıktan Türetilmiş Yakıt: Yasal Çerçeve, Avrupa’daki ve Türkiye’deki Durum", https://dergipark.org.tr/en/download/article-file/613105


# In[5]:


gd1.iloc[2:3,::] = gd1.iloc[2:3,::].apply(lambda x: 300*x/81)
gd2 = gd1.rename(index={'Atıktan Türetilmiş Yakıt Miktarı [ton]': 'Yakıt Üretmek İçin Kullanılan Atık Miktarı[ton]'})


# In[6]:


gd2.round(1) 


# In[7]:


ea=pd.read_csv('ist_evsel_atik_toplam.txt',sep="-")

# In[8]:


ea1=pd.pivot_table(ea, values='Evsel Atık Miktarı[ton]',  columns=['Yıllar'])
ea1


# In[9]:


gdea1 = pd.concat([ea1, gd2], axis=0, join='outer')
gdea1.head(3)


# In[10]:


gdea2=gdea1.dropna(axis='columns')
gdea2


# In[11]:


da_values=[gdea2.iloc[0:1,i]-sum(gdea2.iloc[1:5,i]) for i in range(7)]
dray = np.array( da_values )
dray2=np.reshape(dray, (1,7)) 


# In[12]:


da=pd.DataFrame([[4849056.07407407, 5402945.10774411, 5582060.37373737,
        5683026.1986532 , 6052549.89225589, 5982954.88215488,
        5579298.16835017]],columns=[2009, 2014, 2015, 2016, 2017, 2018, 2019],index=["Düzensiz Biriktirilen Atık Miktarı[ton]"])
da.round(1)


# In[13]:


gdea3 = pd.concat([gdea2, da])
gdea3=gdea3.round(1)
gdea3


# In[14]:


a1=np.zeros((5,7))


# In[15]:


for j in range(0,7):
    for i in range(0,5):
       a1[i,j]=format(gdea3.iloc[i+1,j]/gdea3.iloc[0,j]*100,".2f")
    
a1


# In[19]:


x_pos = np.arange(len(a1[0:5,0]))
x_pos


# In[20]:


fig_size=[14,8]
plt.figure(figsize=fig_size)
x_labels = ['2009', '2014', '2015', '2016', '2017', '2018', '2019']
x_pos = np.arange(len(a1[0,0:7]))

plt.bar(x_pos,a1[4,0:7],color="black")
plt.bar(x_pos,a1[3,0:7],color="b",bottom=a1[4,0:7])
plt.bar(x_pos,a1[2,0:7],color="red",bottom=a1[3,0:7]+a1[4,0:7])
plt.bar(x_pos,a1[1,0:7],color="yellow",bottom=a1[2,0:7]+a1[3,0:7]+a1[4,0:7])
plt.bar(x_pos,a1[0,0:7],color="green",bottom=a1[1,0:7]+a1[2,0:7]+a1[3,0:7]+a1[4,0:7])


plt.title("İstanbul'da Geri Dönüşüm Grafiği")

plt.xticks(x_pos,x_labels);

plt.xlabel("Yıllar")
plt.ylabel("% Atık Miktarı")

plt.legend(["Depolanan Atık Miktarı","Çöp Gazından Elektrik Üretiminde Kullanılan Atık Miktarı",
           "Yakıt Üretmek İçin Kullanılan Atık Miktarı",
           "Geri Dönüşebilir Malzeme Miktarı",
         "Üretilen Kompost Miktarı"])


plt.show();

