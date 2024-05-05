import requests
import urllib.request
import wget
import os
import re
from bs4 import BeautifulSoup
main_dir="./fonts/dafonts/"
if not os.path.exists(main_dir):
    os.makedirs(main_dir)
 
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ#'
attrs = { 'href': re.compile(r'\.mid$') }
# Iterate over the string
page = 1
for element in 'a':
    if not os.path.exists(main_dir + element):
        os.makedirs(main_dir + element)    
    vgm_url = 'https://www.dafont.com/top.php?page=' + str(page) + "&fpp=200"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    result = requests.get(vgm_url , headers=headers)    
    pagetext = result.text
    soup = BeautifulSoup(pagetext, 'html.parser')
    lastpage = soup.find('a', title='Keyboard shortcut: Right arrow').find_previous().text
 
    for x in range(1, int(lastpage)):    
        print(element , "Page: ", x) 
        vgm_url = 'https://www.dafont.com/top.php?page=' + str(x) + "&fpp=200"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        result = requests.get(vgm_url , headers=headers)    
        pagetext = result.text
        soup = BeautifulSoup(pagetext, 'html.parser')            
        mydivs = soup.find_all("div", {"class": "preview"})
        for div in mydivs:
 
            downurl = "https://dl.dafont.com/dl/?f="
            poster = div["style"].replace("background-image:url(/","").replace(")","") 
            downpost = poster.replace(".png",'')
            down = downpost.rsplit('/', 1)[-1]
            down = down[:-1]            
            preurl = "https://www.dafont.com/" + poster            
            
            filename = wget.download(preurl , out = main_dir)            
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(downurl + down, headers=headers)
            try:
                filenamer = r.headers['Content-Disposition'].replace('attachment; filename=','')
                with open(main_dir + filenamer, 'wb') as fh:
                    fh.write(r.content)            
                print(" Downloaded: " + down )
            except:
                print(r.headers)
                with open(main_dir + down + ".zip", 'wb') as fh:
                    fh.write(r.content)
                print(" Downloaded: " + down )