#!/usr/bin/env python
# coding: utf-8

# In[16]:


import scrapy
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML

class AppleCrawler(scrapy.Spider):
    name = "apple"
    start_urls = ["https://tw.nextapple.com/realtime/latest"]

    def parse(self, response):
        
        domain="https://tw.nextapple.com"
        res = BeautifulSoup(response.body.decode('utf-8'), 'html.parser')
        for news in res.select(".post"):
            #title = news.select("h3")[0].text
            #print(domain+news.select("a")[0]["herf"])
            yield scrapy.Request(domain+news.select("a")[0]["herf"],self.parse_detail)#能夠抓取頁面，在進入頁面
            
    def parse_detail(self,response):
        res=BeautifulSoup(response.body.decode('utf-8'), 'html.parser')
        res.select("#h1")[0].text


# In[38]:


cd C:\Users\paylung\LEARNING


# In[ ]:


get_ipython().system('conda create --name myenv')
get_ipython().system('conda activate myenv')


# In[ ]:


conda install -c conda-forge scrapy


# In[35]:


ls


# In[ ]:


dir

