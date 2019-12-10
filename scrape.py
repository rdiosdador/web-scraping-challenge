from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape():

    #Site Navigation
    
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)



    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_paragraph = soup.find("div",class_ ="article_teaser_body").text

    news_title = soup.find("div", class_="content_title").text

    
    #JPL Mars Space Images - Featured Image

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    base_url = 'https://www.jpl.nasa.gov'

    img_url = soup.find(id='full_image').get('data-fancybox-href')

    img_url

    fullimgurl = base_url + img_url

    #get mars weather's latest tweet from the website

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(5)

    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')
    marsweather = soup.find('p', class_= 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text


    #Mars Facts
    
    mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    mars_df.columns=["Description", "Value"]
    mars_df.set_index("Description", inplace=True)
    mars_html = mars_df.to_html()

    #Hemispheres
    
    hemisphere =[]

    hemisphere_list=['Cerberus','Schiaparelli','Syrtis','Valles']

    for hemi in hemisphere_list:
        
        hemispheres={}
        
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

        browser.visit(url)

        time.sleep(5)

        html = browser.html

        soup = BeautifulSoup(html,'html.parser')

        browser.click_link_by_partial_text(hemi)

        html = browser.html

        soup = BeautifulSoup(html,'html.parser')

        hemispheres['image']=soup.find('a',target="_blank")['href']

        hemispheres['title']=soup.find('h2',class_="title").text
        
        hemisphere.append(hemispheres)


    marsinfo={
        'news_title': news_title,
        'news_paragraph':news_paragraph,
        'fullimgurl':fullimgurl,
        'mars_wheather':marsweather,
        'marsfacts_html':mars_html,
        'hemispheres':hemisphere
    }
    return marsinfo
