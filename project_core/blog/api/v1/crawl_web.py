
from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets
import psycopg2

from selenium import webdriver
from ...models import Post
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime

# from jdatetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# import os
# from urllib.parse import urlparse
# import requests
# from .views import NewsViewset


def connection_to_database():
    '''Establishing the connection'''
    conn = psycopg2.connect(database="your data base", user='your user',
                            password='your password', host='your host', port='5432')
    conn.autocommit = True
    return conn


class CrawlViewset(viewsets.ViewSet):
    # Define constant variables
    publisher = 11  # "crawler@gmail.com"
    author = 11  # "crawler@gmail.com"
    type_of_news = 4  # "crawl"
    tags = 11
    isna = 3
    irna = 2
    tasnim = 8
    mehr = 5
    fars = 6
    vezarat = 9
    shoraynegahban = 10

    def xxx_crawl(self, i, wait, folder_name_id):
        try:
            h1 = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='search_results_wrapper']/div["+str(i)+"]/div[1]/div[2]/div[1]/h2/a"))).text
            
            news = Post.objects.filter(h1=h1).first()
            if not (news):
                try:
                    title = h1[0:69]
                    chrome_options = Options()
                    chrome_options.add_argument("--headless")
                    Driver = webdriver.Chrome(options=chrome_options)
                    # Driver = webdriver.Chrome()
                    
                    Driver.get("https://www.xxx.com/")
                    wait1 = WebDriverWait(Driver, 3)
                    
                    search = wait1.until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/header[1]/div[1]/div/div[2]/div/div[2]/div/div/form/input")))
                    search.send_keys(title)
                    search.send_keys(Keys.ENTER)
                    for j in range(1, 10, 1):
                        pathtitle = '//*[@id="search"]/section[2]/div/ul/li['+str(j)+']/div/h3'
                        # Searching for the news title and checking the obtained title with the previous title
                        titlenews = wait1.until(
                            EC.presence_of_element_located((By.XPATH, pathtitle))).text
                        if titlenews[0:15] == title[0:15]:
                            # extract news abstract
                            snippet = wait1.until(EC.presence_of_element_located(
                                (By.XPATH, "//*[@id='search']/section[2]/div/ul/li["+str(j)+"]/div/p[1]"))).text
                            snippet = snippet[0:140]
                            press_link = wait1.until(EC.presence_of_element_located(
                                (By.XPATH, "//*[@id='search']/section[2]/div/ul/li["+str(j)+"]/div/h3/a"))).get_attribute('href')
                            chrome_options = Options()
                            chrome_options.add_argument("--headless")
                            Drivers = webdriver.Chrome(options=chrome_options)
                            # Drivers = webdriver.Chrome()
                            Drivers.get(press_link)
                            wait3 = WebDriverWait(Drivers, 3)
                            
                            image_url = wait3.until(EC.presence_of_element_located(
                                (By.XPATH, "//*[@id='item']/div[2]/div[1]/div[1]/figure/img"))).get_attribute('src')
                            

                            content = wait3.until(EC.presence_of_element_located(
                                (By.XPATH, "//*[@id='item']/div[2]/div[1]/div[1]/div"))).text
                            
                            article_reference = Drivers.current_url
                            article_reference=article_reference[0:39]
                            source_website = self.isna
                            published_date = datetime.now()
                            
                            conn = connection_to_database()
                            cursor = conn.cursor()
                            cursor.execute('''INSERT INTO blog_post (updated_date, created_date, meta_description, ro_titer, slog, folder_name_id, publisher_id, author_id, h1, title, snippet,image_url, content, source_website_id, type_of_news_id, published_date, status,confirm_to_post, trash,counted_views,article_reference) 
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)''',
                                           (published_date, published_date, snippet, '', '', folder_name_id, self.publisher, self.author, title, title, snippet, image_url, content, source_website, self.type_of_news, str(published_date), False, False, False, str(int(1)),article_reference))
                            conn.close()
                            Drivers.close()
                        # else:
                        #     print('not match')
                except Exception as e:
                    raise Exception(
                        "An error occurred in crawl isnanews: " + str(e))
            # else:
            #     print("This content is duplicated")
        except RuntimeError:
            pass

    def yyy_crawl(self, i, wait, folder_name_id):
        try:
            h1 = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='search_results_wrapper']/div["+str(i)+"]/div[1]/div[2]/div[1]/h2/a"))).text
            news = Post.objects.filter(h1=h1).first()
            if not (news):
                try:
                    title = h1[0:69]
                    chrome_options = Options()
                    chrome_options.add_argument("--headless")
                    Driver = webdriver.Chrome(options=chrome_options)
                    # Driver = webdriver.Chrome()
                    Driver.maximize_window()
                    Driver.get("https://www.yyy.com/")
                    wait1 = WebDriverWait(Driver, 5)
                    searchclick = wait1.until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/header/div/div[1]/div[1]/nav/button/i")))
                    searchclick.click()
                    search = wait1.until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/header/div/div[2]/div/div/form/div/input")))
                    search.send_keys(title)
                    search.send_keys(Keys.ENTER)
                    for j in range(1, 10, 1):
                        pathtitle = '//*[@id="mainbody"]/div/div/div/section[2]/div/ul/li['+str(
                            j)+']/div/h3'
                        titlenews = wait1.until(
                            EC.presence_of_element_located((By.XPATH, pathtitle))).text
                        if titlenews[0:15] == title[0:15]:
                            press_link = wait1.until(EC.presence_of_element_located(
                                (By.XPATH, '//*[@id="mainbody"]/div/div/div/section[2]/div/ul/li['+str(j)+']/div/h3/a'))).get_attribute('href')
                            chrome_options = Options()
                            chrome_options.add_argument("--headless")
                            Drivers = webdriver.Chrome(options=chrome_options)
                            # Drivers = webdriver.Chrome()
                            Drivers.get(press_link)
                            wait3 = WebDriverWait(Drivers, 5)
                            snippet = wait3.until(EC.presence_of_element_located(
                                (By.XPATH, "/html/body/main/section/div/div/div/article/p"))).text
                            snippet = snippet[0:140]
                            image_url = wait3.until(EC.presence_of_element_located(
                                (By.XPATH, "//*[@id='item']/figure/a/img"))).get_attribute('src')
                            
                            content = wait3.until(EC.presence_of_element_located(
                                (By.XPATH, "//*[@id='item']/div[3]/div"))).text
                            article_reference = Drivers.current_url
                            article_reference=article_reference[0:34]
                            source_website = self.irna
                            published_date = datetime.now()
                            conn = connection_to_database()
                            cursor = conn.cursor()
                            cursor.execute('''INSERT INTO blog_post (updated_date, created_date, meta_description, ro_titer, slog, folder_name_id, publisher_id, author_id, h1, title, snippet, image_url, content, source_website_id, type_of_news_id, published_date, status,confirm_to_post, trash,counted_views,article_reference) 
                                            VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)''',
                                           (published_date, published_date, snippet, '', '', folder_name_id, self.publisher, self.author, title, title, snippet, image_url, content, source_website, self.type_of_news, str(published_date), False, False, False, str(int(1)),article_reference))
                            conn.close()
                            Drivers.close()
                        # else:
                        #     print('not match')
                except Exception as e:
                    raise Exception(
                        "An error occurred in crawl irnanews: " + str(e))
        # else:
        #     print("This content is duplicated")
        except RuntimeError:
            pass

    def ccc_crawl(self, i, wait, folder_name_id):
        try:
            h1 = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='search_results_wrapper']/div["+str(i)+"]/div[1]/div[2]/div[1]/h2/a"))).text
            news = Post.objects.filter(h1=h1).first()
            if not (news):
                try:
                    title = h1[0:69]
                    chrome_options = Options()
                    chrome_options.add_argument("--headless")
                    Driver = webdriver.Chrome(options=chrome_options)
                    # Driver = webdriver.Chrome()
                    Driver.get("https://www.ccc.com/")
                    wait1 = WebDriverWait(Driver, 3)
                    search = wait1.until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/header/div[1]/div/div/div[2]/div/form/div/input")))
                    search.send_keys(title)
                    search.send_keys(Keys.ENTER)
                    for j in range(1, 5, 1):
                        pathtitle = '/html/body/main/div/div/div/section[2]/div/ul/li['+str(
                            j)+']/div/h3/a'
                        titlenews = wait1.until(
                            EC.presence_of_element_located((By.XPATH, pathtitle))).text
                        if titlenews[0:15] == title[0:15]:
                            press_link = wait1.until(EC.presence_of_element_located(
                                (By.XPATH, "/html/body/main/div/div/div/section[2]/div/ul/li["+str(j)+"]/div/h3/a"))).get_attribute('href')
                            chrome_options = Options()
                            chrome_options.add_argument("--headless")
                            Drivers = webdriver.Chrome(options=chrome_options)
                            # Drivers = webdriver.Chrome()
                            Driver.close()
                            Drivers.get(press_link)
                            wait3 = WebDriverWait(Drivers, 3)
                            snippet = wait3.until(EC.presence_of_element_located(
                                (By.XPATH, "/html/body/main/div/div/div/div/div[1]/article/div[3]/p"))).text
                            snippet = snippet[0:140]
                            image_url = wait3.until(EC.presence_of_element_located(
                                (By.XPATH, "/html/body/main/div/div/div/div/div[1]/article/div[3]/figure/img"))).get_attribute('src')
                            content = wait3.until(EC.presence_of_element_located(
                                (By.XPATH, "/html/body/main/div/div/div/div/div[1]/article/div[4]/div[1]"))).text
                            article_reference = Drivers.current_url
                            source_website = self.mehr
                            published_date = datetime.now()
                            conn = connection_to_database()
                            cursor = conn.cursor()
                            cursor.execute('''INSERT INTO blog_post (updated_date, created_date, meta_description, ro_titer, slog, folder_name_id, publisher_id, author_id, h1, title, snippet, image_url, content, source_website_id, type_of_news_id, published_date, status,confirm_to_post, trash,counted_views,article_reference) 
                                            VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)''',
                                           (published_date, published_date, snippet, '', '', folder_name_id, self.publisher, self.author, title, title, snippet, image_url, content, source_website, self.type_of_news, str(published_date), False, False, False, str(int(1)),article_reference))
                            conn.close()
                            Drivers.close()
                        # else:
                        #     print('not match')
                except Exception as e:
                    raise Exception(
                        "An error occurred in crawl mehrnews: " + str(e))
        # else:
        #     print("This content is duplicated")
        except RuntimeError:
            pass

    
    
    