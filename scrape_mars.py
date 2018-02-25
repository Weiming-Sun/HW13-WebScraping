from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import html.parser
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    nasamarsnewsurl = 'https://mars.nasa.gov/news/'
    response = requests.get(nasamarsnewsurl)
    nasamarsnewssoup = bs(response.text, 'html.parser')
    news_title = nasamarsnewssoup.find_all('div', class_="content_title")[0].a.text.strip('\n')
    news_p = nasamarsnewssoup.find_all('div', class_="rollover_description_inner")[0].text.strip('\n')

    browser = init_browser()
    JPLmarsspaceimageurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPLmarsspaceimageurl)
    html = browser.html
    JPLmarsspaceimagesoup = bs(html, 'html.parser')
    url = JPLmarsspaceimagesoup.find_all('a', class_='fancybox')[0].get("data-fancybox-href")
    featured_image_url = 'https://www.jpl.nasa.gov'+ url
    featured_image_url

    marsweathertwitterurl = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(marsweathertwitterurl)
    marsweathertwittersoup = bs(response.text, 'html.parser')
    mars_weather = marsweathertwittersoup.find_all('div', class_="js-tweet-text-container")[0].p.text

    marsfactsurl = 'https://space-facts.com/mars/'
    marsfactstables = pd.read_html(marsfactsurl)
    marsfactsdf = marsfactstables[0]
    marsfactsdf.columns = ['Facts', 'Details']
    marsfactsdf.set_index('Facts', inplace=True)
    html_table = marsfactsdf.to_html()

    browser = Browser('chrome', headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    astrogeologysoup = bs(html, 'html.parser')
    hemisphere = astrogeologysoup.find_all('div', class_='item')
    hemisphere_image_urls = []
    for hem in hemisphere:
        url = 'https://astrogeology.usgs.gov'+ hem.find('a').get('href')
        soup = bs(requests.get(url).text, 'html.parser')
        dict = {}
        dict["title"] = soup.find("title").text.replace(" Enhanced | USGS Astrogeology Science Center", "")
        dict["img_url"] = soup.find_all('div', class_="downloads")[0].find_all('ul')[0].find_all('li')[1].find('a').get('href')       
        hemisphere_image_urls.append(dict)

    scrapedict = {}

    scrapedict['news_title'] = news_title
    scrapedict['news_p'] = news_p
    scrapedict['featured_image_url'] = featured_image_url
    scrapedict['mars_weather'] = mars_weather
    scrapedict['html_table'] = html_table
    scrapedict['hemisphere_image_urls'] = hemisphere_image_urls

    return scrapedict