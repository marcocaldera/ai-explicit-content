# import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from constant import HYPE_USER, PASSWORD
import time
import urllib.request
from collections import Counter
import numpy as np
import pandas as pd
from common.utilities import init_browser


class ChromeBrowserInfluencerList:

    def __init__(self):
        self.chrome_browser = init_browser()

    def hypeauditor_login(self):
        self.chrome_browser.get('https://hypeauditor.com/login/')
        self.chrome_browser.find_element_by_name("email").send_keys(HYPE_USER)
        self.chrome_browser.find_element_by_name("password").send_keys(PASSWORD)
        self.chrome_browser.find_element_by_xpath('//button[normalize-space()="Log in Send"]').click()
        # time.sleep(3)

    def get_1000_influencers_list(self):
        ranking_list_url = "https://hypeauditor.com/en/top-instagram/?p="
        influencers_list = []
        topic_list = []
        for page in range(0, 20):
            # print(page)
            self.chrome_browser.get(ranking_list_url + str(page + 1))
            html = self.chrome_browser.page_source
            soup_object = BeautifulSoup(html, 'html.parser')  # trasformazione in un oggetto della libreria soup
            table_containing_influencers = soup_object.find('table')
            body = table_containing_influencers.find('tbody')
            for row in body.findAll('tr'):
                user = row.find("a", class_="kyb-ellipsis")
                topic = row.find("span", class_="bloggers-top-topic")
                username = user.decode_contents()
                username = username[1:]
                influencers_list.append(username)
                if topic is not None:
                    topic_list.append(topic.decode_contents())
                else: topic_list.append("")
        return influencers_list, topic_list


start = pd.Timestamp.now()
# code

chrome_browser = ChromeBrowserInfluencerList()
chrome_browser.hypeauditor_login()
time.sleep(1)
influencers_list, topic_list = chrome_browser.get_1000_influencers_list()
frame = pd.DataFrame({
    'name': influencers_list,
    'topic': topic_list
})
frame.to_csv('dataset/influencer.csv')

# code
print(pd.Timestamp.now() - start)
