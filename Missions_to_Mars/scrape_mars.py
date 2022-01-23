# Dependencies
from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
from flask import Flask

# Initiate Flask App
app = Flask(__name__)

# Functions
def init_browser():
   executable_path = {'executable_path': ChromeDriverManager().install()}
   browser = Browser('chrome', **executable_path, headless=False)
   return browser

def scrape():
   browser = init_browser()
   marsData = {}
   
   # Scrape Mars
   marsUrl = 'https://redplanetscience.com/'
   browser.visit(marsUrl)
   marsSoup = bs(browser.html, 'html.parser')
   time.sleep(1)
   marsTitle = marsSoup.find('div', class_='content_title').text
   marsPara = marsSoup.find('div', class_='article_teaser_body').text
   marsData['newsTitle'] = marsTitle
   marsData['newsPara'] = marsPara
   
   # Scrape JPL
   jplUrl = 'https://spaceimages-mars.com/'
   browser.visit(jplUrl)
   jplSoup = bs(browser.html, 'html.parser')
   time.sleep(1)
   featured_image_url = jplUrl + jplSoup.find('img', class_='headerimage')['src']
   marsData['featImg'] = featured_image_url
   
   # Scrape Facts
   mfUrl = 'https://galaxyfacts-mars.com/'
   mfRes = pd.read_html(mfUrl)
   mfDf = mfRes[0]
   mfDf.columns = mfDf.iloc[0]
   mfDf = mfDf[1:]
   mfHTML = mfDf.to_html().replace('\n', '')
   marsData['marsFacts'] = mfHTML
   
   # Scrape Hemis
   hemiUrl = 'https://marshemispheres.com/'
   browser.visit(hemiUrl)
   hemiSoup = bs(browser.html, 'html.parser')
   time.sleep(1)
   
   hemiHrefs = []
   hemiHrefsHTML = hemiSoup.find_all('h3')[:-1]
   for hemiHref in hemiHrefsHTML:
      finalHemi = hemiUrl + hemiHref.find_parent('a')['href']
      hemiHrefs.append(finalHemi)
   
   hemiImgs = []
   for hemiHref in hemiHrefs:
      browser.visit(hemiHref)
      hemiPartSoup = bs(browser.html, 'html.parser')
      hemiTitle = hemiPartSoup.find('h2', class_='title').text
      hemiImg = hemiUrl + hemiPartSoup.find('img', class_='wide-image')['src']
      hemiInfo = {
         "title": hemiTitle,
         "img_url": hemiImg
      }
      hemiImgs.append(hemiInfo)
      time.sleep(1)
   marsData['hemiImgs'] = hemiImgs
   
   #Close Browser
   browser.quit()
   return marsData

if __name__ == '__main__':
   app.run()
