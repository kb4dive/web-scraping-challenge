from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time


def init_browser():
     # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    # # NASA Mars News Site
    # URL of page to be scraped
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)

    time.sleep(1)

    #Create BeautifulSoup object, parse with html parser
    soup = bs(browser.html, 'html.parser')


    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', 'article_teaser_body').text
    #print(news_title)
    #print(news_p)


    # # JPL Mars Space Images - Featured Image 
    url_image = 'https://jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_image)
    time.sleep(1)

    soup=bs(browser.html, 'html.parser')

    #scrape site for image
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    #print(featured_image_url)


    # # Mars Weather
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    time.sleep(1)
    soup = bs(browser.html, 'html.parser')
    mars_weather = soup.find('div', class_='js-tweet-text-container').text
    #print(mars_weather)


    # # Mars Facts
    # Visit the Mars facts webpage and scrape table data into Pandas
    url_facts = "http://space-facts.com/mars/"
    browser.visit(url_facts)
    time.sleep(1)
    soup = bs(browser.html, 'html.parser')

    mars_info = pd.read_html(url_facts)
    mars_info = pd.DataFrame(mars_info[0])
    #mars_info.columns = ['Attribute', 'Value']
    #mars_info.set_index('Attribute', inplace=True)
    #mars_info.head()

    #convert to HTML table
    mars_facts = mars_info.to_html(header = False, index = False)
    #mars_facts.replace('\n', '')
    #mars_facts

    #save table to file
    #mars_facts.to_html('Mars_table.html')


    # # Mars Hemispheres
    # Visit the USGS Astogeology site and scrape pictures of the hemispheres
    url_hemisphere = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemisphere)
    time.sleep(5)
    soup=bs(browser.html, 'html.parser')


    #Create empty dictionary
    hemisphere_image_urls  = []

    #Point to hemisphere product block
    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    #loop through each of the hemispheres
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        soup=bs(browser.html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "image_url": image_url})
        

    #create the collection for the database   
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "featured_image_url": featured_image_url,
        "hemisphere_image_urls":hemisphere_image_urls
    }


    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data


