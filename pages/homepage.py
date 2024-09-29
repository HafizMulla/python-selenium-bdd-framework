import time

from pages.BasePage import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    """ This class contains all the Home Features Methods """

    PAGE_LOADING_ID = (By.XPATH, "//main[@id='main']")
    REGION_XPATH = (By.XPATH, "//body[contains(@class,'region-content')]")
    MAIN_MENU_XPATH = (By.XPATH, "//*[contains(@class,'navbar-nav')]")
    SEARCH_BLOCK_XPATH = (By.XPATH, "//div[@class='search-widget-main-panel mobile-filters-hidden']")
    MAIN_CONTENT_BLOCK_XPATH = (By.XPATH, "//div[@id='region-main-content']")
    DESTINATION_MAP_CLASSNAME = (By.XPATH, "//div[contains(@class,'sunsail-svg-map-resize-processed')]")
    FOOTER_CLASSNAME = (By.CLASS_NAME, "site-footer")

    search_result = ""

    """Constructor of HomePage class"""

    def __init__(self, driver):
        super().__init__(driver)

    def validate_title(self, title):
        assert self.get_title() == title

    def is_page_loaded(self):
        return self.verify_element_displayed(self.PAGE_LOADING_ID)

    def page_loaded_without_error(self):
        self.verify_element_displayed(self.REGION_XPATH)

    def is_main_menu_displayed(self):
        return self.verify_element_displayed(self.MAIN_MENU_XPATH)

    def is_hero_block_loaded(self):
        return self.verify_element_displayed(self.HERO_BLOCK_CLASSNAME)

    def is_search_block_loaded(self):
        return self.verify_element_displayed(self.SEARCH_BLOCK_XPATH)

    def is_main_content_displayed(self):
        return self.verify_element_displayed(self.MAIN_CONTENT_BLOCK_XPATH)

    def is_destination_map_displayed(self):
        return self.verify_element_displayed(self.DESTINATION_MAP_CLASSNAME)

    def is_footer_displayed(self):
        return self.verify_element_displayed(self.FOOTER_CLASSNAME)

