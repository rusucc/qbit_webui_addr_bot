from api_key import TOKEN, ID
import home_functions
import json
import requests
import urllib.parse
from time import sleep

# TODO docstrings for each function

URL = "https://api.telegram.org/bot{}/".format(TOKEN)


# Make request to Telegram servers and returns content from the HTTP GET
def get_url(url):
    print(url)
    try:
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content
    except requests.exceptions.ConnectionError:
        print('Connection error! Retrying in 30 secs.')
        sleep(30)
        return get_url(url)


# Gets content returned from get_url() and parses as a json structure
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


# Creates a connection to Telegram servers (that renews each 100 sec) which gets each new message/chat update
# Uses an update_id as offset to specify the last update received, that way getting only the latest new messages
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


# Gets last chat id and text from the update json received
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id


# Append each update in an array, and returns the highest number id which is always the latest
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


# Sends the message to chat
def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


# Treats each update received
def update_treatment(updates):
    for update in updates["result"]:
        # Checks if message came from me
        if update["message"]["from"]["id"] == int(ID):
            try:
                text = update["message"]["text"]
                message_to_send = home_functions.function_selector(text.lower())
                chat = update["message"]["chat"]["id"]
                send_message(message_to_send, chat)
            except Exception as e:
                print(e)
        # If message is not sent by my user (checking chat id), replies telling that does not have permission
        else:
            chat = update["message"]["chat"]["id"]
            send_message('Você não é o Danilo =(', chat)
            send_message('You are not allowed to do that.', chat)
