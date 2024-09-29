""" This file contains all the home page related feature script  """

import os
from behave import *
from selenium import webdriver
# from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import traceback
# noinspection PyUnresolvedReferences
from pages.HomePage import HomePage
from Utilities.Utils import Utilities


@given('The browser is launched')
def launch_browser(context):
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    if os.getenv('HEADLESS') is None or os.getenv('HEADLESS') != 'false':
        options.add_argument("--headless")

    # to supress the error messages/logs
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    context.driver = webdriver.Chrome(service=service,options=options)

    context.driver.implicitly_wait(10)


@given('I have navigated to the "{url}" page')
@when('I have navigated to the "{url}" page')
def open_yachts(context, url):
    try:
        context.driver.get(os.getenv("ROOT_URL") + url)
        context.homePage = HomePage(context.driver)
        context.utils = Utilities(context.driver)

        context.utils.check_cookie_status()
    except:
        context.driver.close()
        assert False, "Test is failed in open login page section."


@when('The base page has loaded')
@then('The base page has loaded')
def page_loaded(context):

    try:
        assert context.homePage.is_page_loaded() is True

    except Exception as exception_error:
        assert False, f'Test is failed as the page is not loaded.{traceback.format_exc(),exception_error}'


@then('The page should display with no errors')
def step_impl(context):
    try:
        context.homePage.page_loaded_without_error()

    except Exception as exception_error:
        assert False, f"Test is failed as the page was displayed with errors " \
                      f"main menu was not displayed.{traceback.format_exc(),exception_error}"


@then('The main menu should display')
def step_impl(context):
    try:
        assert context.homePage.is_main_menu_displayed() is True

    except Exception as exception_error:
        assert False, f"Test is failed as the main menu was not displayed.{traceback.format_exc(),exception_error}"


@then('The search block should display')
def search_block_should_display(context):
    try:
        assert context.homePage.is_search_block_loaded() is True

    except Exception as exception_error:
        assert False, f"Test is failed as Search block is not loaded.{traceback.format_exc(),exception_error}"


@then('The main content should display')
def step_impl(context):
    try:
        assert context.homePage.is_main_content_displayed() is True

    except Exception as exception_error:
        assert False, f"Test is failed in validate login page title.{traceback.format_exc(),exception_error}"


@then('destination map should display')
def step_impl(context):
    try:
        assert context.homePage.is_destination_map_displayed() is True

    except Exception as exception_error:
        assert False, f"Test is failed in validate login page title.{traceback.format_exc(),exception_error}"


@then('the footer should display')
def step_impl(context):
    try:
        assert context.homePage.is_footer_displayed() is True

    except Exception as exception_error:
        assert False, f"Test is failed in validate login page title.{traceback.format_exc(),exception_error}"

