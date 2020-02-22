import pandas as pd
from bs4 import BeautifulSoup
import json
import os
import time
from constant import USERNAME, PASSWORD, INSTA_PASSWORD_NEW, INSTA_USERNAME_NEW
from common.utilities import init_browser


class ChromeBrowserInfluencerData:

    def __init__(self):
        self.chrome_browser = init_browser()
        self.prepare_folder_for_influencer_json()

    @staticmethod
    def prepare_folder_for_influencer_json():
        influencer_json_folder = './dataset/influencer-json/'
        if not os.path.exists(influencer_json_folder):
            os.makedirs(influencer_json_folder)

    def instagram_login(self):
        self.chrome_browser.get('https://www.instagram.com/accounts/login')
        time.sleep(1)
        self.chrome_browser.find_element_by_name("username").send_keys(INSTA_USERNAME_NEW)
        self.chrome_browser.find_element_by_name("password").send_keys(INSTA_PASSWORD_NEW)
        self.chrome_browser.find_element_by_xpath('//button[normalize-space()="Log In"]').click()
        time.sleep(5)

    def outline_user(self, user):
        influencer_profile_url = "https://www.instagram.com/" + user
        print(influencer_profile_url)

        # Recupero script
        self.chrome_browser.get(influencer_profile_url)
        html = self.chrome_browser.page_source
        soup_object = BeautifulSoup(html, 'html.parser')
        body = soup_object.find('body')
        script_tag = body.find('script')

        # Gestione json
        raw_string_with_json_data = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        user_json_data = json.loads(raw_string_with_json_data)

        # Salvataggio del json su disco
        with open('dataset/influencer-json-2020/' + user + '.json', 'w') as f:
            json.dump(user_json_data, f)


start = pd.Timestamp.now()
# code

chrome_browser = ChromeBrowserInfluencerData()
chrome_browser.instagram_login()
username_list = pd.read_csv('./dataset/influencer.csv')

for index, user in username_list.iterrows():
    # break
    if index >= 935:
        if index % 10 == 0:
            print(index)
            time.sleep(10)
        chrome_browser.outline_user(user[1])
    # chrome_browser.outline_user(user[1])
    # time.sleep(2)
# code
print(pd.Timestamp.now() - start)
# info TEMPO DI ESECUZIONE: 0 days 00:17:08.794233
