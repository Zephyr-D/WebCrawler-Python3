# -*- coding: utf-8 -*-
"""
WebCrawler for Tieba

Created on Wed Mar  2 11:57:55 2016

@author: ZephyrD

@environment: Windows 10
"""

import urllib.request as request
import re
import urllib.error as error

# Function for Downloading
def baidu_tieba(url, begin_page, end_page):
    count = 1
    for i in range(begin_page, end_page):
        m = request.urlopen(url+str(i)).read()
        page_data = m.decode('utf-8')  # for Windows
        page_image = re.compile('<img class="BDE_Image" src=\"(.+?)\"')
        for image in page_image.findall(page_data):
            pattern = re.compile(r'^http://.*.jpg$')
            if  pattern.match(image):
                try:
                    image_data = request.urlopen(image).read()
                    image_path = dirpath + '/' + str(count) + '.jpg'
                    count += 1
                    print(image_path)
                    with open(image_path, 'wb') as image_file:
                        image_file.write(image_data)
                    image_file.close()
                except error.URLError as e:
                    print('Download failed')

# Data Input
dirpath = 'YOUR PATH'
url = "http://tieba.baidu.com/p/xxxxxxxx?pn="
begin_page = 1
end_page = 2

# Run
baidu_tieba(url, begin_page, end_page)





