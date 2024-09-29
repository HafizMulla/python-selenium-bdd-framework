import os
import copy
import requests

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from Utilities.payload import Payload
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('SLACK_BOT_TOKEN')
# fetching the Demo cancel reservation api key to access Demo
DEMO_API_KEY = os.getenv('Demo_API_KEY')
message_thread = None


class SlackBot:

    def __init__(self):
        self.client = WebClient(token=TOKEN)
        # Now instead of hard-coding the slack channel id, we are now capturing it through environmental variable
        # self.channel_id = "C04AXQ01797"  # slack group id: bots-dx-yachts(C04AXQ01797) and bots-dx-test (C03NTE1GN5Q)
        self.channel_id = os.getenv('SLACK_CHANNEL_ID')
        self.message_ts = None
        self.message_ts2 = None

    def post_file_on_slack(self, log_files=None, msg_text=""):
        global message_thread

        if message_thread:
            thread_ts = message_thread
        else:
            thread_ts = None

        try:
            payload = copy.deepcopy(Payload.BLOCKS)
            divider = copy.deepcopy(Payload.DIVIDER)
            mark_down = copy.deepcopy(Payload.MARK_DOWN)

            mark_down['text']['text'] = msg_text

            payload['blocks'].append(divider)
            payload['blocks'].append(mark_down)
            payload['blocks'].append(divider)

            print('Sending and uploading file message using Bot..')
            response = self.client.files_upload(
                channels=self.channel_id,
                file=log_files,
                initial_comment=msg_text,
                thread_ts=thread_ts,
                blocks=payload['blocks']
            )
            if response.status_code == 200:
                print("Successfully completed posting file on slack "
                              "and status code %s" % response.status_code)
            else:
                print("Failed to post report on slack "
                              "and status code %s" % response.status_code)

        except SlackApiError as e:
            print("Error uploading file: {}".format(e))

    def post_message_on_slack(self, text=""):
        global message_thread

        try:
            payload = copy.deepcopy(Payload.BLOCKS)
            divider = copy.deepcopy(Payload.DIVIDER)
            mark_down = copy.deepcopy(Payload.MARK_DOWN)
            mark_down['text']['text'] = text
            payload['blocks'].append(divider)
            payload['blocks'].append(mark_down)
            payload['blocks'].append(divider)

            if text:
                print('Sending message using Bot')
                response = self.client.chat_postMessage(
                    channel=self.channel_id,
                    text=text,
                    thread_ts=self.message_ts,
                    blocks=payload['blocks']
                )
                self.message_ts = response.data['ts']
                message_thread = self.message_ts

                if response.status_code == 200:
                    print("Successfully completed posting message on slack and status code %s" % response.status_code)
                else:
                    print("Failed to post report on slack and status code %s" % response.status_code)

        except SlackApiError as e:
            print("Error uploading file: {}".format(e))

    def cancel_check(self, Check_id):
        print(f"check number:{Check_id}\n")
        if check_id is not None:
            check_id = (check_id.split(":")[1]).strip()
            print(f"\ncancel url:{Demo_CANCEL_URL} and Check number:{book_id}\n")
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': Demo_API_KEY
            }

            payload_data = {
                "brand": "SUN",
                "CheckReference": book_id,
                "reason": ""
            }

            response_data = requests.post(Demo_CANCEL_URL, headers=headers, json=payload_data)

            response = response_data.json()

            print(f"response:{response_data.text}")
            print(f"response.text:{response['status_code']} and {response['message']} and "
                  f"{response['data']['CancellationResponse']}\n")

            if response['status_code'] == 200 and "Error" not in response['data']['CancellationResponse']:
                response_message = f"The check cancellation is successful with the status code:{response['status_code']} " \
                                   f"and message:{response_data.text}"
            else:
                response_message = f"we got error with the status code:{response['status_code']} " \
                                   f"and message:{response_data.text}"

        else:
            response_message = "Check reference number is not generated"

        return response_message
