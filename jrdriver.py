from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import logging


logger = logging.getLogger()


class JrDriver:
    def __init__(self, options, default_wait):
        self.options = options
        self.default_wait = default_wait
        self.driver = self.setup()
        self.driver.implicitly_wait(self.default_wait)

    def setup(self):
        if type(self.options) == Options:
            return webdriver.Chrome(options=self.options)

        chrome_options = Options()

        if type(self.options) == list:
            for option in self.options:
                chrome_options.add_argument(option)
        elif type(self.options) == str:
            chrome_options.add_argument(self.options)
        else:
            raise TypeError('Invalid Options object. Must be of type Options, List, or String')
        return webdriver.Chrome(options=chrome_options)

    def input_value(self, x_path, value):
        element = self.find_element(x_path)
        element.send_keys(str(value))

    def find_element(self, x_path):
        web_elements = self.driver.find_elements_by_xpath(x_path)
        if web_elements:
            web_element = web_elements[0]
            if len(web_elements) > 1:
                logger.warning('xpath:{} returned multiple web elements: {}'.format(x_path, web_elements))
            return web_element
        else:
            raise NoSuchElementException('Element with xpath "{}" not found.'.format(x_path))

    def goto(self, url):
        self.driver.get(url)

    def click_element_if_exists(self, x_path):
        try:
            web_element = self.find_element(x_path)
            web_element.click()
            return True
        except NoSuchElementException:
            self.driver.save_screenshot('./screenshots/'+str(datetime.datetime.now())+'.png')
            logging.warning('Element with xpath "{}" not found. Unable to click on element.'.format(x_path))
            return False

    def screenshot(self, path='./screenshots/' + str(datetime.datetime.now()) + '.png'):
        self.driver.save_screenshot(path)

    def tear_down(self):
        self.driver.close()

    def get_href_from_element(self, x_path):
        element = self.find_element(x_path)
        href = element.get_attribute('href')
        return href

    def hover_over_element(self, x_path):
        element = self.find_element(x_path)
        ActionChains(self.driver).move_to_element(element).perform()

    def get_length(self, x_path):
        return len(self.find_element(x_path))

    def login(self, url, user, user_x_path, pwd, pwd_x_path, enter_x_path):
        self.goto(url)
        self.input_value(user_x_path, user)
        self.input_value(pwd_x_path, pwd)
        self.click_element_if_exists(enter_x_path)

