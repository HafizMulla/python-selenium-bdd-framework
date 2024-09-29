""" This file contains all the utilities scripts """
import base64
import os
import time
import datetime
import cv2
import traceback

from Utilities.Slackbot import SlackBot


class Utilities:

    def __init__(self, driver=None):
        self.driver = driver

    def take_screenshot(self, file_name):
        try:
            slackbot = SlackBot()

            current_date_time = str(datetime.datetime.now())
            image_date_time = current_date_time.replace(" ", "_").replace(":", "_").replace(",", "_").split('.')[0]
            screenshot_image = "Screenshot_"+str(file_name)+"_"+str(image_date_time)+".png"
            final_screenshot = "screenshots\\"+self.fullpage_screenshot(screenshot_image)

            final_url = self.get_current_url()
            current_page_source = self.driver.page_source
            test_failure_log = "logs\\Page_source_log_"+str(file_name)+"_"+str(image_date_time)+".txt"
            test_backend_log = "logs\\Backend_log_"+str(file_name)+"_"+str(image_date_time)+".txt"

            with open(test_failure_log, "w") as text_file:
                text_file.write("Current url: %s" % final_url)
                text_file.writelines("\n\nPage Source: %s price" % current_page_source.encode('utf-8'))

            # Disabling this as it is only used on local
            # self.get_backend_details(test_backend_log)

            print("Sharing failure Screenshot")
            slackbot.post_file_on_slack(final_screenshot)
            print("Sharing failure Page source")
            slackbot.post_file_on_slack(test_failure_log)
            # print("Sharing failure Backend log")
            # slackbot.post_file_on_slack(test_backend_log)

        except Exception as e:
            print("Exception raised while taking screenshot:{}{}".format(traceback.format_exc(),e))

    def convert_image_to_base64(self, base64_image):
        with open(base64_image, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read())
        return b64_string

    def fullpage_screenshot(self, filename):
        """ This method take full screenshot """
        total_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
        viewport_height = self.driver.execute_script('return window.innerHeight')
        total_width = self.driver.execute_script('return document.body.offsetWidth')
        viewport_width = self.driver.execute_script("return document.body.clientWidth")

        # this implementation assume (viewport_width == total_width)
        assert(viewport_width == total_width)

        # scroll the page, take screenshots and save screenshots to slices
        offset = 0  # height
        loop_count = 1
        image_list = []
        while offset < total_height:
            if offset + viewport_height > total_height:
                offset = total_height - viewport_height

            self.driver.execute_script('window.scrollTo({0}, {1})'.format(0, offset))
            time.sleep(0.3)
            image_name = loop_count
            task_image = str(image_name) + '.png'
            image_list.append(task_image)
            self.driver.save_screenshot('screenshots\\' + task_image)
            loop_count = loop_count + 1
            offset = offset + viewport_height

        # combine image slices into single image
        images = []
        for image in image_list:
            images.append(cv2.imread('screenshots\\'+image))

        concatenated_image = cv2.vconcat(images)
        cv2.imwrite('screenshots\\'+filename, concatenated_image)

        # deleting the single snapshot images
        self.delete_screenshot_images(image_list)
        return filename

    def delete_screenshot_images(self, image_list):
        for image in image_list:
            os.remove('screenshots\\'+image)

    def get_current_url(self):
        """ This method return the current page url"""

        current_page_url = self.driver.current_url

        if 'd2' in current_page_url:
            split_text = current_page_url.split('@')
            end_point = split_text[0].split('d2')
            final_url = end_point[0]+split_text[1]
        else:
            final_url = self.driver.current_url

        return final_url

    def get_backend_details(self, file_name):
        """ This method is used to add the backend details of the failure step in the file """

        with open(file_name, "w") as text_file:
            header_text = "request.url :\t request.response.status_code :\t request.response.headers['Content-Type']"
            text_file.writelines(header_text + "\n")
            for request in self.driver.requests:
                if request.response:
                    text_file.writelines(
                        str(request.url) + " :\t " +
                        str(request.response.status_code) + " :\t " +
                        str(request.response.headers['Content-Type']) + "\n"
                    )

    def get_refine_test_report(self):
        """ This method is used to remove the extra printing of the selenium wire console log from the report file """
        try:
            with open('t2.txt', "r") as file_input:
                with open('reports\\reg_test_reports.txt', "w") as output:
                    for line in file_input:
                        if line.find('INFO:seleniumwire.') == -1:
                            output.write(line)

            file_input.close()
            print("Extra text is now removed")

        except Exception as e:
            print("Error occurred while refining the test report:{} {}".format(traceback.format_exc(),e))

    def disabled_abtasty_on_current_page(self, status=False):
        """ This method is used to disable the ABTasty on the browser on single page
         Parameters:
             status(boolean): by default set to "False", to disable the ABtasty set it to "True".
         """
        print("Cookies status before")
        self.check_cookie_status()
        if status:
            print("----Disabling the ABTasty----")
            self.driver.execute_script('document.cookie = "ABTastyOptout=1"')
            print("----Reloading the page----")
            self.driver.execute_script('location.reload();')
        print("----Cookies status after----")
        self.check_cookie_status()

    def check_cookie_status(self, show_details=False):
        """ This method is used to get the browser cookie details
        Parameter:
            show_details(boolean): By default set to "False",to see the cookie details set it to "True".
        """
        cookies = self.driver.execute_script('return document.cookie')
        if show_details:
            print("cookie:", cookies)
        if "ABTastyOptout=1" in cookies:
            print("\n---ABtasty status: ABtasty is disabled\n")
        else:
            print("\n---ABtasty status: ABtasty is enabled\n")

        return cookies
