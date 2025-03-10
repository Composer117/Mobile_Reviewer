from selenium import webdriver
from selenium.webdriver.common.by import By
from contextlib import closing
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
#import urllib2
import urllib.request,urllib.parse,urllib.error
import re
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd

data_alll=[]

def remove_non_ascii_1(text):

    return ''.join([i if ord(i) < 128 else ' ' for i in text])

with closing(webdriver.Firefox()) as browser:
    site = "https://www.flipkart.com/redmi-note-5-pro-black-64-gb/product-reviews/itmf2fc3xgmxnhpx?page=1&pid=MOBF28FTQPHUPX83"
    browser.get(site)

    file = open("Review.txt", "w")

    for count in range(1, 13):
        nav_btns = browser.find_elements_by_class_name('_2Xp0TH')
        
        button = ""

        for btn in nav_btns:
            number = int(btn.text)
            if(number==count):
                button = btn
                break

        button.send_keys(Keys.RETURN)
        WebDriverWait(browser, timeout=10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_2xg6Ul")))

        read_more_btns = browser.find_elements_by_class_name('_1EPkIx')
		

        for rm in read_more_btns:
            browser.execute_script("return arguments[0].scrollIntoView();", rm)
            browser.execute_script("window.scrollBy(0, -150);")
            rm.click()

        page_source = browser.page_source
        #print(page_source)

        soup = BeautifulSoup(page_source, "lxml")
        ans = soup.find_all("div", class_="_1PBCrt")


        for tag in ans:
            data_loop=[]
            title = tag.find("p", class_="_2xg6Ul").string
            title = remove_non_ascii_1(title)
            #data_loop.append(title)
            
            content = tag.find("div", class_="qwjRop").div.prettify().replace(u"\u2018", "'").replace(u"\u2019", "'")
            content = remove_non_ascii_1(content)
            #print("Hi",content)
            content.encode('ascii','ignore')
            #print("HiH",content)
            content = content[24:-35]
            #print("HiHi",content)
            content=re.sub('<.+>',' ',content)
            data_loop.append(content)
            

            votes = tag.find_all("span", class_="_1_BQL8")
            upvotes = int(votes[0].string)
            downvotes = int(votes[1].string)
            #data_loop.append(upvotes)
            #data_loop.append(downvotes)
            
            data_alll.append(data_loop)
            file.write("Review Title : %s\n\n" % title )
            file.write("Upvotes : " + str(upvotes) + "\n\nDownvotes : " + str(downvotes) + "\n\n")
            file.write("Review Content :\n%s\n\n\n\n" % content )


file.close()
dataset = pd.DataFrame(data_alll)
#headers = ['Review Title', 'Review Content', 'Upvotes', 'Downvotes']
headers = ['Review Content']
dataset.columns = headers
#dataset.sample(3)

#dataset.to_csv("Review.csv", index = False)
dataset.to_csv("Review(Content - Redmi Note 5 Pro).csv", index = False)