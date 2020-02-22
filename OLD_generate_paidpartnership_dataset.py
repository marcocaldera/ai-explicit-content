import pandas as pd
from bs4 import BeautifulSoup
import json
import os
import time
from constant import USERNAME, PASSWORD, INSTA_PASSWORD_NEW, INSTA_USERNAME_NEW
from common.utilities import init_browser
import numpy as np
from selenium.common.exceptions import NoSuchElementException
import string
from selenium.webdriver.common.keys import Keys
import re
import urllib.request


class GeneratePaidPartnershipDataset:

    def __init__(self):
        self.chrome_browser = init_browser(watch=True)
        self.prepare_folder_for_influencer_json()
        self.post_object = []

    @staticmethod
    def prepare_folder_for_influencer_json():
        influencer_json_folder = './dataset/influencer-json/'
        if not os.path.exists(influencer_json_folder):
            os.makedirs(influencer_json_folder)

    def instagram_login(self):
        self.chrome_browser.get('https://www.instagram.com/accounts/login')
        time.sleep(1)
        self.chrome_browser.find_element_by_name("username").send_keys(USERNAME)
        self.chrome_browser.find_element_by_name("password").send_keys(PASSWORD)
        self.chrome_browser.find_element_by_xpath('//button[normalize-space()="Log In"]').click()
        time.sleep(3)

    @staticmethod
    def __clean_comment(comment):
        hashtag = [word for word in comment.split() if word.startswith('#')]  #  prendo hashtag
        tag = [word for word in comment.split() if word.startswith('@')]  # prendo tag

        comment = " ".join([word for word in comment.split() if word not in hashtag])  # rimuovo hashtag
        comment = " ".join([word for word in comment.split() if word not in tag])  # rimuovo tag
        comment = comment.translate(str.maketrans('', '', string.punctuation))  # rimuovo punteggiatura

        return hashtag, tag, comment

    def __get_label(self):
        try:
            self.chrome_browser.find_element_by_class_name("y1ezF._8XEIW")
            return "paid"
        except NoSuchElementException as e:
            return "standard"

    def __get_numbers_of_likes(self):
        try:
            likes = self.chrome_browser.find_element_by_class_name('Nm9Fw').text
        except NoSuchElementException as e:
            self.chrome_browser.find_element_by_class_name('vcOH2').click()
            likes = self.chrome_browser.find_element_by_class_name('vJRqr').text
        return re.sub('\D', '', likes)

    def __download_image(self, name):
        try:
            url = self.chrome_browser.find_element_by_class_name('FFVAD').get_attribute('src')
        except NoSuchElementException as e:  # video
            url = self.chrome_browser.find_element_by_class_name('_8jZFn').get_attribute('src')

        print("url: ", url)
        urllib.request.urlretrieve(url, "dataset/images/{}.jpg".format(name))

    def get_post(self, user, index):
        """
        Trovare 10 post sponsorizzati e 10 non per utente
        :param user:
        :return:
        """
        influencer_profile_url = "https://www.instagram.com/" + user
        print(influencer_profile_url)
        self.chrome_browser.get(influencer_profile_url)
        time.sleep(10)
        body = self.chrome_browser.find_element_by_tag_name("body")
        # Click sulla prima foto
        self.chrome_browser.find_element_by_class_name("v1Nh3.kIKUG._bz0w").click()

        time.sleep(1)

        for i in range(10):
            print(user + str(i))

            text = None
            while text is None or len(text) == 1:
                time.sleep(5)
                try:
                    text = self.chrome_browser.find_element_by_class_name('C4VMK').text.split('\n')
                    print(text)

                    if text[0] == user:
                        hashtag, tag, comment = self.__clean_comment(" ".join(text[1:]))

                        likes = self.__get_numbers_of_likes()

                        self.__download_image(user + str(i))

                        self.post_object.append({
                            "user": text[0],
                            "image_id": user + str(i),
                            "hashtag_list": hashtag,
                            "tag_list": tag,
                            "comment": comment,
                            # "hashtag_count": len(hashtag),
                            # "tag_count": len(tag),
                            # "comment_count": len(comment.split()),
                            "likes": likes,
                            "label": self.__get_label()
                        })

                        print("-" * 100)

                except NoSuchElementException as e:
                    print(e)
                    pass

            body.send_keys(Keys.ARROW_RIGHT)


chrome_browser = GeneratePaidPartnershipDataset()
chrome_browser.instagram_login()

username_list = pd.read_csv('./dataset/influencer.csv')
for index, user in username_list.iterrows():
    chrome_browser.get_post(user[1], index)
    break

frame = pd.DataFrame(chrome_browser.post_object)
frame.to_csv('dataset/partnership.csv')
