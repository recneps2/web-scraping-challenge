import pandas as pd
import requests
import html
import time
from bs4 import BeautifulSoup
from splinter import Browser

executable_path = {"executable_path": "chromedriver"}

def scrape_info():

    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)

    time.sleep(2)

    soup = BeautifulSoup(browser.html,'html.parser')

    results = soup.find('div', class_='list_text').a.text

    n_para = soup.find('div', class_='article_teaser_body').text
        
    mars = {
        'News_Title' : results,
        'News_Para' : n_para,
    }

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    browser.links.find_by_partial_href("/images").click()

    time.sleep(2)
    soup = BeautifulSoup(browser.html, 'html.parser')
    featured_image = soup.find(class_='BaseImage').get('src')
    mars["featured_img"] = featured_image


    url = 'https://space-facts.com/mars/'

    m_facts = pd.read_html(url)

    m_clean = m_facts[0]

    m_clean.columns = ["Description" , "Values"]

    html_table = m_clean.to_html(index=False)

    html_table = html_table.replace('\n', '')

    mars["Facts"] = html_table


    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)

    hemisphere_image_urls = []

    for i in range(4):
        
        hemisphere = {}
        
        browser.find_by_css("a.product-item h3")[i].click()
        
        soup = BeautifulSoup(browser.html, 'html.parser')
        
        title = soup.find("h2", class_='title').get_text()
        
        img = soup.find("a", text = "Sample").get("href")
        
        hemisphere["title"] = title
        
        hemisphere["img_url"] = img
        
        hemisphere_image_urls.append(hemisphere)
        
        browser.back()
        
    hemisphere_image_urls
    
    browser.quit()

    mars["Hemisphere_Image_URLS"] = hemisphere_image_urls

    return mars

if __name__ == "__main__":
    print(scrape_info()) 