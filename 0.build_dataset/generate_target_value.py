from constant import USERNAME, PASSWORD, INSTA_PASSWORD_NEW, INSTA_USERNAME_NEW
from common.utilities import init_browser
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json


class GenerateTargetValue:
    def __init__(self):
        self.chrome_browser = init_browser(watch=False)
        self.instagram_login()

    def instagram_login(self):
        self.chrome_browser.get('https://www.instagram.com/accounts/login')
        time.sleep(1)
        self.chrome_browser.find_element_by_name("username").send_keys(USERNAME)
        # self.chrome_browser.find_element_by_name("username").send_keys(INSTA_USERNAME_NEW)
        self.chrome_browser.find_element_by_name("password").send_keys(PASSWORD)
        # self.chrome_browser.find_element_by_name("password").send_keys(INSTA_PASSWORD_NEW)
        self.chrome_browser.find_element_by_xpath('//button[normalize-space()="Log In"]').click()
        time.sleep(5)

    def get_target_value(self, user, url_first_image):
        influencer_profile_url = "https://www.instagram.com/" + user
        self.chrome_browser.get(influencer_profile_url)
        time.sleep(5)
        body = self.chrome_browser.find_element_by_tag_name("body")

        # Mi porto sulla prima foto utile dell'album
        url_first_image_id = url_first_image.split('/')[-1].split('?')[0]
        # print(url_first_image_id)
        photos_list = self.chrome_browser.find_elements_by_class_name("v1Nh3.kIKUG._bz0w")
        for i in range(6):
            url_photo = photos_list[i].find_element_by_class_name('FFVAD').get_attribute('src')
            url_photo_id = url_photo.split('/')[-1].split('?')[0]

            if url_photo_id == url_first_image_id:
                photos_list[i].click()
                break

        label_list = []
        for i in range(12):
            time.sleep(10)
            label_list.append(self.__get_label())
            body.send_keys(Keys.ARROW_RIGHT)
            # self.outline_user(user, i)

        print(label_list)
        return label_list

    # def __get_url_image(self):
    #     try:
    #         url = self.chrome_browser.find_element_by_class_name('FFVAD').get_attribute('src')
    #     except NoSuchElementException as e:  # video
    #         url = self.chrome_browser.find_element_by_class_name('tWeCl').get_attribute('poster')
    #     return url

    # def outline_user(self, user, i):
    #     html = self.chrome_browser.page_source
    #     soup_object = BeautifulSoup(html, 'html.parser')
    #     body = soup_object.find('body')
    #     script_tag = body.find('script')
    #
    #     # Gestione json
    #     raw_string_with_json_data = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
    #     user_json_data = json.loads(raw_string_with_json_data)
    #
    #     # Salvataggio del json su disco
    #     with open('dataset/influencer-test/' + user + str(i) + '.json', 'w') as f:
    #         json.dump(user_json_data, f)
    #
    #     return user_json_data

    def __get_label(self):
        try:
            self.chrome_browser.find_element_by_class_name("y1ezF._8XEIW")
            return "paid"
        except NoSuchElementException as e:
            return "standard"
