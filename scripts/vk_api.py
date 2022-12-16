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


class Wall(Api):
    def get_comments(self):  # wall.getComments
        pass

    def delete_comment(self):  # wall.deleteComment
        pass

    def get_posts(self):  # wall.get
        pass


class Group(Api):
    def delete_message(self):  # messages.delete
        pass

    def get_messages(self):  # messages.getHistory
        pass


class Discussion(Api):
    def delete_comment(self):  # board.deleteComment
        pass

    def get_discussions(self):  # board.getTopics
        pass

    def get_comments(self):  # board.getComments
        pass


api = Api()
