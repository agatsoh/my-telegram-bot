from bottle import (
    run, post, response, request as bottle_request
)
import requests
import json

with open('config.json') as config_file:
    config = json.load(config_file)

BOT_URL = f"https://api.telegram.org/bot{config['telegram_token']}/"


def get_chat_id(data):
    """
    Method to extract chat id from telegram request.
    """
    chat_id = data['message']['chat']['id']
    return chat_id


def get_message(data):
    """
    Method to extract message id from telegram request.
    """
    message_text = data['message']['text']
    return message_text


def prepare_answer(data):
    message = get_message(data)
    answer = "What are you saying ?"
    if message in ['hi', 'hello', 'how are you']:
        answer = 'welcome'
    json_data = {
        'chat_id': get_chat_id(data),
        'text': answer,
    }
    return json_data


def send_message(prepared_data):
    message_url = BOT_URL+'sendMessage'
    requests.post(message_url, json=prepared_data)


@post('/')  # our python function based endpoint
def main():
    data = bottle_request.json  # <--- extract all request data
    answer_data = prepare_answer(data)
    send_message(answer_data)  # <--- function for sending answer
    return response


if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
