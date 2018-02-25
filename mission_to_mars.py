
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import html.parser
import pandas as pd


# In[ ]:


# URL of page to be scraped
nasamarsnewsurl = 'https://mars.nasa.gov/news/'

# Retrieve page with the requests module
response = requests.get(nasamarsnewsurl)

# Create BeautifulSoup object; parse with 'html.parser'
nasamarsnewssoup = bs(response.text, 'html.parser')
#print(nasamarsnewssoup.prettify())


# In[ ]:


news_title = nasamarsnewssoup.find_all('div', class_="content_title")[0].a.text.strip('\n')
news_title


# In[ ]:


news_p = nasamarsnewssoup.find_all('div', class_="rollover_description_inner")[0].text.strip('\n')
news_p


# In[ ]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
#browser = Browser('chrome', headless=False)

JPLmarsspaceimageurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(JPLmarsspaceimageurl)

html = browser.html
JPLmarsspaceimagesoup = bs(html, 'html.parser')


# In[ ]:


url = JPLmarsspaceimagesoup.find_all('a', class_='fancybox')[1].get("data-fancybox-href")
featured_image_url = 'https://www.jpl.nasa.gov'+ url
featured_image_url


# In[ ]:


# URL of page to be scraped
marsweathertwitterurl = 'https://twitter.com/marswxreport?lang=en'

# Retrieve page with the requests module
response = requests.get(marsweathertwitterurl)

# Create BeautifulSoup object; parse with 'html.parser'
marsweathertwittersoup = bs(response.text, 'html.parser')
#print(nasamarsnewssoup.prettify())


# In[ ]:


mars_weather = marsweathertwittersoup.find_all('div', class_="js-tweet-text-container")[0].p.text
mars_weather


# In[ ]:


marsfactsurl = 'https://space-facts.com/mars/'
marsfactstables = pd.read_html(marsfactsurl)
marsfactstables


# In[ ]:


marsfactsdf = marsfactstables[0]
marsfactsdf.columns = ['Facts', 'Details']
marsfactsdf.set_index('Facts', inplace=True)
html_table = marsfactsdf.to_html()
html_table.replace('\n', '')


# In[ ]:


browser = Browser('chrome', headless=False)
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
html = browser.html
astrogeologysoup = bs(html, 'html.parser')
hemisphere = astrogeologysoup.find_all('div', class_='item')


# In[ ]:


hemisphere_image_urls = []

for hem in hemisphere:
    url = 'https://astrogeology.usgs.gov'+ hem.find('a').get('href')
    soup = bs(requests.get(url).text, 'html.parser')
    dict = {}
    dict["title"] = soup.find("title").text.replace(" Enhanced | USGS Astrogeology Science Center", "")
    dict["img_url"] = soup.find_all('div', class_="downloads")[0].find_all('ul')[0].find_all('li')[1].find('a').get('href')
    
    hemisphere_image_urls.append(dict)

hemisphere_image_urls

