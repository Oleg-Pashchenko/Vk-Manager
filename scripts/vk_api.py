import json
import threading

from vk_maria import Vk, types
from vk_maria.dispatcher import Dispatcher


class Bot:
    def __init__(self, vk):
        self.dp = Dispatcher(vk)

        @self.dp.message_handler()
        def echo(event: types.Message):
            event.answer(event.message.text)

        self.dp.start_polling()


class Api:
    def __init__(self):
        self.token = self.read_token()
        self.vk = Vk(access_token=self.token)
        x = threading.Thread(target=Bot, args=(self.vk,))
        x.start()

    @staticmethod
    def read_token():
        return json.loads(open('../secrets.json', 'r').read())['token']

    def get_comments(self):
        pass

    def delete_comment(self):
        pass

    def get_discutions(self):
        pass


api = Api()
