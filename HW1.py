#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import random
import matplotlib.pyplot as plt
plt.rc("font",family="Microsoft JhengHei")
#上方表示可以顯示出中文

df=pd.read_csv("chia_yi_edu.csv",encoding="utf-8")
df.isnull().sum().sum()


# In[2]:


#df


# In[3]:


#問題一:國中國小各幾所？
type_list=[]
for i in df["校名"]:
    if("國小"in i):
        type_list.append("國小")
    else:
        type_list.append("國中")
df["國中小"]=type_list


# In[4]:


from collections import Counter
element_counts = Counter(type_list)
print("嘉義國小的數量：", element_counts["國小"])
print("嘉義國中的數量：", element_counts["國中"])
print("嘉義國中小的總數為：", element_counts["國中"]+element_counts["國小"])


# In[5]:


#問題二:千人大校有哪些？
# 創建一個空的列表來存放結果
student_more_1000 = []

# 遍歷DataFrame的每一行
for index, row in df.iterrows():
    # 檢查每個年度的學生數是否都超過1000
    all_years_more_than_1000 = all(row[f"{year}學年度"] > 1000 for year in range(101, 112))
    if all_years_more_than_1000:
        # 如果所有年度的學生數都超過1000，將學校名稱加入結果列表
        student_more_1000.append(row["校名"])

# 列印結果
print("所有年度都超過1000的學校有：")
print(student_more_1000)


# In[6]:


# 創建兩個空的列表來存放符合條件的國小和國中
more_1000_ele = []
more_1000_jun = []

# 遍歷DataFrame的每一行
for index, row in df.iterrows():
    # 檢查每個年度的學生數是否都超過1000
    all_years_more_than_1000 = all(row[f"{year}學年度"] > 1000 for year in range(101, 112))
    if all_years_more_than_1000:
        # 如果所有年度的學生數都超過1000，根據校名的標識判斷是國小還是國中
        if "國小" in row["校名"]:
            more_1000_ele.append(row["校名"])
        elif "國中" in row["校名"]:
            more_1000_jun.append(row["校名"])

# 列印結果
print("所有年度都超過1000的學校：")
print(f"符合條件的國小有：{more_1000_ele}")
print(f"符合條件的國中有：{more_1000_jun}")


# In[7]:


#問題三:各學年度350人以內的學校有哪些？
# 創建兩個空的字典，用來存放符合條件的國小和國中學校
less_350_ele = {}
less_350_jun = {}

# 遍歷DataFrame的每一行
for year in range(101, 112):  # 從101學年度到111學年度
    # 清空字典，以便儲存當前年度的結果
    less_350_ele[year] = []
    less_350_jun[year] = []

    # 檢查當前年度的學生人數是否低於350
    for index, row in df.iterrows():
        if row[f"{year}學年度"] < 350:
            # 根據校名的標識判斷是國小還是國中，並將學校名稱加入對應的列表
            if "國小" in row["校名"]:
                less_350_ele[year].append(row["校名"])
            elif "國中" in row["校名"]:
                less_350_jun[year].append(row["校名"])

# 列印結果
for year in range(101, 112):
    print(f"{year}學年度學生人數低於350的學校：")
    print(f"低於350人的國小有：{less_350_ele[year]}")
    print(f"低於350人的國中有：{less_350_jun[year]}")
    print("-" * 50)  # 分隔不同學年度的結果


# In[8]:


#匯入學校資訊
df2=pd.read_csv("school_infor.csv",encoding="utf-8")
#df2


# In[9]:


#校名修改
# 修改校名中的文字
df2['校名'] = df2['校名'].str.replace('國民小學', '國小').str.replace('國民中學', '國中')
#df2


# In[10]:


#問題4:東西區的學校各有幾所
# 假設 df2 是包含「校名」和「校址」兩列的 DataFrame

# 判斷校址中包含西區的學校有幾所
西區學校數量 = df2[df2['校址'].str.contains('西區')]['校名'].count()

# 判斷校址中包含東區的學校有幾所
東區學校數量 = df2[df2['校址'].str.contains('東區')]['校名'].count()

print("西區的學校有", 西區學校數量, "所")
print("東區的學校有", 東區學校數量, "所")


# In[11]:


pip install geopy


# In[12]:


pip install --upgrade pip


# In[13]:


pip install opencage


# In[14]:


import tkinter as tk
from geopy.geocoders import OpenCage


# In[15]:


pip show opencage


# In[28]:


pip install folium


# In[29]:


pip install folium --upgrade


# In[35]:


#獲取地址經緯度的方法，但因為沒辦法把地圖顯示出來這次就先不用了
import folium
from opencage.geocoder import OpenCageGeocode

# 替換成你的 OpenCage API 金鑰
api_key = '816db6b77c8d46799309a12596a0c6ab'

# 創建 OpenCageGeocode 實例
geocoder = OpenCageGeocode(api_key)

# 使用 geocoder 進行地理編碼
results = geocoder.geocode('嘉義市西區世賢路四段141號')

# 獲取緯度和經度
latitude = results[0]['geometry']['lat']
longitude = results[0]['geometry']['lng']


# In[34]:


# 在 df2 表單中新增經度和緯度的欄位
df2['Longitude'] = None
df2['Latitude'] = None

# 遍歷 DataFrame，獲取校址的經度和緯度並填入 DataFrame
for index, row in df2.iterrows():
    location = row['校址']
    try:
        results = geocoder.geocode(location)
        latitude = results[0]['geometry']['lat']
        longitude = results[0]['geometry']['lng']
        df2.at[index, 'Longitude'] = longitude
        df2.at[index, 'Latitude'] = latitude
    except Exception as e:
        print(f"Error: {e} for address: {location}")

# 檢視更新後的 df2 表單
print(df2)


# In[36]:


#df2


# In[38]:


#問題5:各國中最接近的國小前幾名
from geopy.distance import great_circle
from collections import defaultdict

# 假設 df2 是包含「校名」、「Longitude」和「Latitude」三列的 DataFrame

# 找取所有「國中」的學校的經緯度坐標
國中學校 = df2[df2['校名'].str.contains('國中')]
國中學校經緯度 = list(zip(國中學校['Latitude'], 國中學校['Longitude']))

# 找取所有「國小」的學校的經緯度坐標
國小學校 = df2[df2['校名'].str.contains('國小')]
國小學校經緯度 = list(zip(國小學校['Latitude'], 國小學校['Longitude']))

# 找出每個國中學校前三名最近的國小學校及距離
最近學校 = defaultdict(list)
for 國中 in 國中學校經緯度:
    for 國小 in 國小學校經緯度:
        距離 = great_circle(國中, 國小).kilometers
        最近學校[國中].append((國小學校.iloc[國小學校經緯度.index(國小)]['校名'], 距離))
    最近學校[國中].sort(key=lambda x: x[1])  # 按距離由小到大排序
    # 確保每所國小只出現一次
    seen = set()
    最近學校[國中] = [(國小, 距離) for 國小, 距離 in 最近學校[國中] if 國小 not in seen and not seen.add(國小)][:3]  # 只保留前三名

# 輸出結果
for 國中, 最近三個學校 in 最近學校.items():
    print('國中學校: {}'.format(國中學校.iloc[國中學校經緯度.index(國中)]['校名']))
    for 國小, 距離 in 最近三個學校:
        print('  最近的國小學校: {}，距離: {:.2f} 公里'.format(國小, 距離))


# In[40]:


# 將 "Longitude" 和 "Latitude" 欄位轉換為浮點數格式
df2['Longitude'] = df2['Longitude'].astype(float)
df2['Latitude'] = df2['Latitude'].astype(float)


# In[41]:


#問題7:各國小最接近的國中？
from collections import defaultdict
from geopy.distance import great_circle

# 處理資料清理和標準化（例如，將學校名稱轉換為小寫，去除空格等）
df2['校名'] = df2['校名'].str.lower().str.strip()

國小學校 = df2[df2['校名'].str.contains('國小')]
國小學校經緯度 = list(zip(國小學校['Latitude'], 國小學校['Longitude']))

國中學校 = df2[df2['校名'].str.contains('國中')]
國中學校經緯度 = list(zip(國中學校['Latitude'], 國中學校['Longitude']))

最近學校 = defaultdict(list)
for 國小 in 國小學校經緯度:
    for 國中 in 國中學校經緯度:
        距離 = great_circle(國小, 國中).kilometers
        最近學校[國小].append((國中學校.iloc[國中學校經緯度.index(國中)]['校名'], 距離))
    最近學校[國小].sort(key=lambda x: x[1])
    最近學校[國小] = 最近學校[國小][:2]

# 輸出結果
for 國小, 最近兩個學校 in 最近學校.items():
    print('國小學校: {}'.format(國小學校.iloc[國小學校經緯度.index(國小)]['校名']))
    for 國中, 距離 in 最近兩個學校:
        print('  最接近的國中學校: {}，距離: {:.2f} 公里'.format(國中, 距離))


# In[42]:


#問題8:顯示各年度段國小國中的總人數
df['學校類型'] = df['校名'].apply(lambda x: '國小' if '國小' in x else '國中')

# 计算各学年度“國小”和“國中”的总人数
guoxiao_totals = df[df['學校類型'] == '國小'].filter(like='學年度').sum()
guozhong_totals = df[df['學校類型'] == '國中'].filter(like='學年度').sum()

# 输出结果
print("國小各學年度總人數：")
print(guoxiao_totals)
print("國中各學年度總人數：")
print(guozhong_totals)


# In[43]:


#問題9：年度之間的人數成長百分比
for i in range(101, 111):
    # 计算当前学年度与下一学年度的人数成长百分比
    current_col = f"{i}學年度"
    next_col = f"{i + 1}學年度"
    
    # 创建新的一列，存放人数成长百分比
    df[f"{i}-{i + 1}成長百分比"] = ((df[next_col] - df[current_col]) / df[current_col]) * 100

# 只保留校名和人数成长百分比列，并输出结果
result_df = df[['校名'] + [f"{i}-{i + 1}成長百分比" for i in range(101, 111)]]
print(result_df)


# In[44]:


#result_df


# In[45]:


#問題10:找出成長百分比超過30或低於-30的校名和相對應的成長百分比
for index, row in result_df.iterrows():
    school_name = row['校名']
    for col in result_df.columns[1:]:  # 從第二個欄位開始檢查，因為第一個是校名
        growth_rate = row[col]
        if growth_rate > 30 or growth_rate < -30:
            print(f"學校名稱: {school_name}, 成長百分比({col}): {growth_rate}")


# In[ ]:


pip install matplotlib


# In[46]:


import matplotlib.pyplot as plt

# 假設您的數據框名稱為df，並且第一列是校名，第二列到第十二列是101學年度到111學年度的人數
# 請確保數據框df已經準備好

# 提取校名和學年度的數據
schools = df.iloc[:, 0]
years = df.columns[1:12]

# 提取人數數據（從第二列到第十二列）
data = df.iloc[:, 1:12]

# 繪製折線圖
plt.figure(figsize=(12, 6))

# 使用不同的顏色繪製每個校名的折線
for i in range(len(schools)):
    plt.plot(years, data.iloc[i], marker='o', label=schools[i])

# 添加標籤和標題
plt.xlabel('學年度')
plt.ylabel('人數')
plt.title('不同校名的人數變化趨勢')
plt.xticks(rotation=45)  # 將x軸標籤旋轉為45度，以避免重疊

# 添加圖例
plt.legend()

# 顯示圖表
plt.tight_layout()
plt.show()


# In[47]:


#問題10:顯示出國中/小的學生人數趨勢圖
import matplotlib.pyplot as plt

# 假設您的數據框名稱為df，並且第一列是校名，第二列到第十二列是101學年度到111學年度的人數
# 請確保數據框df已經準備好

# 提取校名和學年度的數據
schools = df.iloc[:, 0]
years = df.columns[1:12]

# 提取人數數據（從第二列到第十二列）
data = df.iloc[:, 1:12]

# 繪製折線圖
plt.figure(figsize=(12, 6))

# 繪製國中的折線圖
for i in range(len(schools)):
    if "國中" in schools[i]:  # 判斷校名是否包含"國中"
        plt.plot(years, data.iloc[i], marker='o', label=schools[i])

# 添加標籤和標題
plt.xlabel('學年度')
plt.ylabel('人數')
plt.title('國中學校的人數變化趨勢')
plt.xticks(rotation=45)  # 將x軸標籤旋轉為45度，以避免重疊

# 添加圖例
plt.legend()

# 顯示圖表
plt.tight_layout()
plt.show()

# 繪製國小的折線圖
plt.figure(figsize=(12, 6))

for i in range(len(schools)):
    if "國小" in schools[i]:  # 判斷校名是否包含"國小"
        plt.plot(years, data.iloc[i], marker='o', label=schools[i])

# 添加標籤和標題
plt.xlabel('學年度')
plt.ylabel('人數')
plt.title('國小學校的人數變化趨勢')
plt.xticks(rotation=45)  # 將x軸標籤旋轉為45度，以避免重疊

# 添加圖例
plt.legend()

# 顯示圖表
plt.tight_layout()
plt.show()


# In[ ]:




