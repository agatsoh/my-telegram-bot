import requests
import json
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from api.raiden_api import RaidenApi
app = Flask(__name__)
api = Api(app)
# parser = reqparse.RequestParser()


class FlaskHandlerMixin:
    def __init__():
        self.BOT_URL = None

    def get_chat_id(self, data):
        """
        Method to extract chat id from telegram request.
        """
        chat_id = data['message']['chat']['id']
        return chat_id

    def get_message(self, data):
        """
        Method to extract message id from telegram request.
        """
        message_text = data['message']['text']
        return message_text

    def send_message(self, prepared_data):
        """
        Prepared data should be json which includes at least `chat_id` and `text`
        """
        message_url = self.BOT_URL + 'sendMessage'
        requests.post(message_url, json=prepared_data)


class TelegramBot(FlaskHandlerMixin, Resource):
    # BOT_URL = 'https://api.telegram.org/bot000000000:aaaaaaaaaaaaaaaaaaaaaaaaaa/'

    def __init__(self, *args, **kwargs):
        with open('config.json') as config_file:
            config = json.load(config_file)
        self.BOT_URL = f"https://api.telegram.org/bot{config['telegram_token']}/"
        self.raiden_node_api = RaidenApi(config['raiden_rpc'])
        self.token_address = '0x46E75a569Be6BdDe5d5E8351c5c035e8DfEa5C62'

    def process_message(self, message):
        arr = message.split()
        if arr[0] == '/pay':
            target_address = arr[1]
            amount = arr[2]
            response = self.raiden_node_api.payments(
                self.token_address,
                target_address,
                amount)
            if response.status_code == 200:
                return "Payment Successful"
            else:
                return "Payment Unsuccessfull please check your message"
        elif arr[0] == '/balance':
            partner_address = arr[1]
            response = self.raiden_node_api.getBalance(
                self.token_address,
                partner_address)
            if response.status_code == 200:
                return response.json()['balance']
        else:
            return "What are you saying"

    def prepare_data_for_answer(self, data):
        message = self.get_message(data)
        # answer = "What are you saying"
        # if message in ['hi', 'hello', 'how are you']:
        #    answer = 'welcome'
        if message == 'test':
            answer = "It works"
        else:
            answer = self.process_message(message)
        chat_id = self.get_chat_id(data)
        json_data = {
            "chat_id": chat_id,
            "text": answer,
        }
        return json_data

    def post(self):
        data = request.json
        answer_data = self.prepare_data_for_answer(data)
        self.send_message(answer_data)
        return 200


api.add_resource(TelegramBot, '/')

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
