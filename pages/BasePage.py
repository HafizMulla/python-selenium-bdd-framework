from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSelectorException as EX
from dotenv import load_dotenv

"""This class is the parent of all the page classes"""

load_dotenv()


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def click_element(self, by_locator):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(by_locator))
            self.driver.execute_script("arguments[0].click();", element)
        except EX as e:
            print("Exception! Can't click on the element")

    def input_element(self, by_locator, text):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(by_locator)).send_keys(text)
        except EX as e:
            print("Exception! Can't click on the element")

    def get_element_text(self, by_locator):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(by_locator)).text

    def get_title(self):
        return self.driver.title

    def get_element_presence(self, by_locator):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(by_locator))

    def get_element_to_be_clickable(self, by_locator, message=''):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(by_locator), message)

    def get_element_attribute(self, by_locator, attribute_name):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(by_locator)).get_attribute(attribute_name)

    def verify_element_displayed(self, by_locator):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(by_locator)).is_displayed()
        except:
            return False

    def wait_until_url_contains(self, by_locator):
        return WebDriverWait(self.driver, 10).until(EC.url_contains(by_locator))

    def wait_until_url_not_contains(self, by_locator):
        return WebDriverWait(self.driver, 10).until_not(EC.url_contains(by_locator))

    def wait_until_element_not_present(self, element):
        return WebDriverWait(self.driver, 10).until_not(EC.presence_of_element_located(element))

    def wait_until_element_not_visible(self, element):
        return WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located(element))
