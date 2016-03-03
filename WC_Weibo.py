# -*- coding: utf-8 -*-
"""
WebCrawler for Weibo

Created on Tue Feb 23 11:59:11 2016

@author: ZephyrD

@environment: Windows 10
"""

from bs4 import BeautifulSoup
import requests
from lxml import etree
import urllib.request as request
import re
import os

# Input message
user_id = (int)('xxxxxxxxx')  # 'xxxxx' for the Weibo ID of your target
cookie = {
   "Cookie": "xxxxxxxxxxxxxxxxxxxxxxxxxxx"  # login to the page on which you are to use the crawler and find your Cookie, you may use Chrome's DevTool ('Network')
}
headers = {
   'User-Agent' : 'xxxxxxxxxxxxxxxxxxx'  # find your headers to act like a browser
}
save_path = "xxxxxxxxxx" + str(user_id)  # your save path
if os.path.exists(save_path) is False:  # create path
    os.mkdir(save_path)

# Preparation
urlog = 'http://weibo.cn/u/' + str(user_id) + '?filter=1' # one's original weibo
html = requests.get(urlog, cookies = cookie).content
selector = etree.HTML(html)
pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
result = "" 
urllist_set = set()
word_count = 1
image_count = 1
print(u'Web Crawler standing by.')

# Get information
for page in range(1,pageNum+1):
  url = urlog + '&page=' + str(page)  # get html
  lxml = requests.get(url, cookies = cookie).content
  # for text
  selector = etree.HTML(lxml)
  content = selector.xpath('//span[@class="ctt"]')
  for each in content:
    text = each.xpath('string(.)')
    if word_count>=4:
      text = "%d :"%(word_count-3) +text+"\n\n"
    else :
      text = text+"\n\n"
    result = result + text
    word_count += 1
  # for images
  soup = BeautifulSoup(lxml, "lxml")
  urllist = soup.find_all('a',href=re.compile(r'^http://weibo.cn/mblog/oripic',re.I))
  first = 0
  for imgurl in urllist:
    urllist_set.add(requests.get(imgurl['href'], cookies = cookie).url)
    image_count +=1
print(u'User\'s data captured.')

# Save text
with open(save_path + "/text.txt",'wb') as fo:
    fo.write(result.encode())
fo.close()
print( u'Text saved, %d original weibo, at %s'%(word_count-4,save_path))

# Save images
if not urllist_set:
  print(u'NO IMAGE')
else:
  # Download
  x=1
  for imgurl in urllist_set:
    temp= save_path + '/%s.jpg' % x
    print( u'Downloading image No. %s' % x)
    try:
      image_data = request.urlopen(imgurl).read()
      with open(temp, 'wb') as image_file:
           image_file.write(image_data)
      image_file.close()
    except:
      print( u"Download failed %s"%imgurl)
    x+=1
print( u'%d images saved, at %s'%(image_count-1,save_path))









