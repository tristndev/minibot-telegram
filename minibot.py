import json
import requests
import urllib.parse
import glob
from os import path, getenv
import time
from dotenv import load_dotenv
import sys
import argparse

class MiniBot(object):
    """Main class for MiniBot logic."""

    def __init__(self, debug=False):
        load_dotenv()
        # BOT CONFIG
        self.TOKEN = getenv("TOKEN")
        self.URL = "https://api.telegram.org/bot{}/".format(self.TOKEN)
        # USER CONFIG
        self.USER_ID = getenv("USER_ID")
        self.debug = debug


    def get_url(self, url):
        """Sends a GET request to a given url.

        Args:
            url (str): URL to send the GET request to

        Returns:
            str: content of GET request. 
        """
        if self.debug:
            print_debug("Sending GET to URL: {}".format(url))
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    def get_json_from_url(self, url):
        """Wrapper to get a JSON object from a URL.

        Args:
            url (str): URL to send the GET request to

        Returns:
            dict: JSON dictionary
        """
        content = self.get_url(url)
        js = json.loads(content)
        return js

    def get_updates(self):
        """Wrapper to get and check updates from the Telegram Bot URL.

        Returns:
            dict: updates from the Telegram Bot API
        """
        url = self.URL + "getUpdates"
        js = self.get_json_from_url(url)
        return self.check_updates(js)
    
    def check_updates(self, upd):
        """Checks whether an update dict is okay. Exits if that is not the case.

        Args:
            upd (dict): update object to check

        Returns:
            dict: checked update dict
        """
        if upd['ok']:
            return upd
        else:
            print_error("Error returned in http response: {} - {}".format(upd['error_code'], upd['description']))
            if upd['error_code'] == 404:
                print_error("Did you set up the .env file correctly?")
            sys.exit(1)

    def get_last_chat_id_and_text(self, updates):
        """Returns the last message received and its sender's user id.

        Args:
            updates (dict): updates dict

        Returns:
            (str, str) tuple: (text, chat_id) tuple 
        """
        num_updates = len(updates["result"])
        if num_updates == 0:
            print_error("Your bot has not received any messages yet.")
            sys.exit(1)
        last_update = num_updates - 1
        
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return text, chat_id

    def send_message(self, text, chat_id=None):
        """Sends a message to a given user id. Send to standard user id if None.

        Args:
            text (str): message to be sent
            chat_id (str, optional): destination user id. Defaults to None.
        """
        if chat_id is None:
            chat_id = self.USER_ID
        parsed_text = urllib.parse.quote(text)
        url = "{}sendMessage?text={}&chat_id={}&parse_mode=html".format(self.URL, parsed_text, chat_id)
        if self.debug:
            print_debug("Sending message to ID {}: {}".format(chat_id, parsed_text))
        content = self.get_json_from_url(url)
        self.check_updates(content)

    def send_dictionary(self, dict, msg=None, chat_id=None):
        """Converts a dictionary (key-value pairs) into a string and sends it.

        Args:
            dict (dict): dictionary to be sent
            msg (str, optional): optional message text to be inserted at beginning of sent message. Defaults to None.
            chat_id (str, optional): destination user id. Defaults to None.
        """
        text = ((msg + "\n") if msg is not None else "") + self.dictionary_to_msg(dict)
        self.send_message(text, chat_id)

    def dictionary_to_msg(self, print_dict):
        """Transforms a dictionary into a message string (one key-value pair per line)

        Args:
            print_dict (dict): dictionary to transform

        Returns:
            str: string of dict contents 
        """
        longest_key_length = max([len(x) for x in print_dict.keys()])
        n_indent = longest_key_length + 3
        lines = []
        for key in print_dict:
            lines.append("<code>{}{}{}</code>".format(key, " "*(n_indent-len(key)), str(print_dict[key])))
        return "\n".join(lines)

    def print_last_chat_id(self):
        """Print the last received message's sender user id."""
        upd = self.get_updates()
        chat_id = self.get_last_chat_id_and_text(upd)[1]

        print_output("The last received message came from USER_ID: {}".format(chat_id))

"""
 >> Helper functions 
"""
def print_error(msg, *argv):
    """Prints an error message.

    Args:
        msg (str): error message to print
    """
    try: 
        argv[0]
        print("## Error: "+msg, argv)
    except:
        print("## Error: "+msg)
            
def print_output(msg, *argv):
    """Prints a normal output message.

    Args:
        msg (str): output message to print
    """
    try: 
        argv[0]
        print(">> " + msg, argv)
    except:
        print(">> " + msg)

def print_debug(msg, *argv):
    """Prints a debug message.

    Args:
        msg (str): debug message to print
    """
    try: 
        argv[0]
        print("-- " + msg, argv)
    except:
        print("-- " + msg)

def print_mode(mode):
    """Prints a chosen mode

    Args:
        mode (str): mode to be printed
    """
    print("// " + mode)

def collect_info_into_message():
    """Placeholder function for information collection.

    Returns:
        str: information to be sent in the Telegram message.
    """
    # Do your info collection here.
    # For example: Look for a log file and extract some info. 
    return "Your collected information."


"""
 >> Cronjob Mode Code 
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Your Python Minibot for Telegram.')
    parser.add_argument('--userid', '-u', 
                        action='store_true', 
                        help="Prints the last USER_ID your bot received a message from.")
    
    parser.add_argument('--dotenv', '-d',
                        action='store_true',
                        help="Prints the information that is stored in the .env file.")

    parser.add_argument('--test', '-t',
                        help="Send a test message from bot to the specified user id.")
    args = parser.parse_args()

    mb = MiniBot()

    if args.userid:
        print("// User ID Mode")
        mb.print_last_chat_id()
        sys.exit()

    if args.dotenv:
        print("// .env mode")
        print("    Token:", mb.TOKEN)
        print("    USER_ID:", mb.USER_ID)
        sys.exit()

    if args.test:
        print("// test mode (debugging active)")
        mb.debug=True
        msg = args.test
        mb.send_message(msg)
        sys.exit()
    
    print("// Standard mode")
    # Define what the bot is supposed to do here and create a string.
    text = collect_info_into_message()

    mb.send_message(text, mb.USER_ID)

    print("all work done.")