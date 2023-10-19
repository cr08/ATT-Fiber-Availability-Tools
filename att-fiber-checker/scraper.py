import json
import requests
import sys
import argparse
from datetime import datetime
from slacker import Slacker
from discordwebhook import Discord

def cleanFilename(sourcestring,  removestring ="\`/<>\:\"\\|?*"):
    return ''.join([c for c in sourcestring if c not in removestring])

parser = argparse.ArgumentParser(description='Checks the configured addresses for availability of '
                                             'ATT Fiber and optionally posts the results to Slack and/or Discord')

parser.add_argument('-d', '--debug', action='store_true', dest='debug', help='Enables debug logging to stdout and saves full json response file.',
                    required=False)

parser.add_argument('-n', '--nofiber', required=False, action='store_true', dest='nofiber', help='Send notification to Slack/Discord if no fiber is available. No messages are posted if no fiber is available by default.')

args = parser.parse_args()

nofiber_notify = args.nofiber
debug = args.debug

# Load config file for Slack/Discord credentials
try:
    with open("config.json", 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print('File config.json does not exist. Printing results to terminal only.')
    config = {}

# Load address list json file
add = {}
with open("addresses.json", 'r') as f:
    add = json.load(f)

availability_url = 'https://www.att.com/services/shop/model/ecom/shop/view/unified/qualification/service' \
                   '/CheckAvailabilityRESTService/invokeCheckAvailability'

for address in add['addresses']:

    json_data = {
        'userInputZip': address['addr_zip'],
        'userInputAddressLine1': address['addr_line'],
        'mode': 'fullAddress',
        'customer_type': 'Consumer',
        'dtvMigrationFlag': False
    }
    headers = {'content-type': 'application/json'}
    fiber_avail = False

    print("Checking \033[1;33m" + address['addr_line'] + ", " + address['addr_zip'] + "\033[1;0m...  ", end="", flush=True)

    try:
        resp = requests.post(availability_url, data = json.dumps(json_data), headers = headers)
        if debug:
            today = datetime.now()
            iso_date = today.isoformat()
            print("DEBUG: Writing json response file - " + cleanFilename(iso_date) + ".json")
            with open(cleanFilename(iso_date) + ".json", "w") as f:
                f.write(resp.text)
        resp_json = json.loads(resp.text)
        fiber_avail = resp_json['profile']['isGIGAFiberAvailable']
    except:
        print("Unexpected error:", sys.exc_info()[0])

    if fiber_avail:
        print("\033[1;32mFiber IS available!\033[1;0m")
    else:
        print("\033[1;31mFiber is NOT available.\033[1;0m")

    if "slack" in config:
        slack = Slacker(config['slack']['slack_key'])

        if fiber_avail:
            msg = "Fiber is available!!"
            txt = ":tada:"
            color = "#33c653"
            attachment = {"text": txt,"color": color}
            slack.chat.post_message(config['slack']['slack_channel'], msg, as_user='AT&T Bot', username='attbot',attachments=[attachment])
            if debug:
                print("DEBUG: Sending Slack message that fiber is available")
        elif nofiber_notify:
            msg = "Fiber isn't available yet :("
            txt = ":cry: :cry: :cry: :cry: :cry:"
            color = "#f44242"
            attachment = {"text": txt,"color": color}
            slack.chat.post_message(config['slack']['slack_channel'], msg, as_user='AT&T Bot', username='attbot',attachments=[attachment])
            if debug:
                print("DEBUG: Sending Slack message that fiber is NOT available")
        else:
            if debug:
                print("DEBUG: Fiber not available and 'nofiber' argument not set. Not sending message to Slack.")
    else:
        if debug:
            print("DEBUG: Slack credentials not set in config. Skipping Slack notification pass.")

    if "discord" in config:
        disc_wh = Discord(url=config['discord']['webhook_url'])

        if fiber_avail:
            if debug:
                print("DEBUG: Sending Discord message that fiber is available")
            disc_wh.post(content="YAY! Fiber IS available at `" + address['addr_line'] + ", " + address['addr_zip'] + "`")
        elif nofiber_notify:
            if debug:
                print("DEBUG: Sending Discord message that fiber is NOT available")
            disc_wh.post(content="Fiber is NOT available at `" + address['addr_line'] + ", " + address['addr_zip'] + "`")
        else:
            if debug:
                print("DEBUG: Fiber not available and 'nofiber' argument not set. Not sending message to Discord.")
    else:
        if debug:
            print("DEBUG: Discord webhook url not set in config. Skipping Discord notification pass.")
