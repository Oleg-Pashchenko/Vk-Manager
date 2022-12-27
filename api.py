import json
import os
import time

import requests

from scripts import links_filter, dirty_words_filter


class Api:
    def __init__(self):
        tokens = self.read_tokens()
        self.group_token = tokens["group_token"]
        self.user_token = tokens["user_token"]
        self.group_id = tokens["group_id"]

    # url example 'https://oauth.vk.com/authorize?client_id=51512754&display=page&scope=groups+wall+board&response_type=token&v=5.131'

    @staticmethod
    def read_tokens():
        return json.loads(open("../secrets.json", "r").read())

    def _make_request(self, method, params):
        params["access_token"] = self.user_token
        params["v"] = "5.131"
        return requests.post(
            url="https://api.vk.com/method/" + method, data=params
        ).json()


class Wall(Api):
    def get_comments(self, post_id):  # wall.getComments
        return self._make_request(
            method="wall.getComments",
            params={"owner_id": -self.group_id, "post_id": post_id},
        )['response']['items']

    def delete_comment(self, comment_id):  # wall.deleteComment
        response = self._make_request(
            method="wall.deleteComment",
            params={"owner_id": -self.group_id, "comment_id": comment_id},
        )
        print(response)

    def get_posts(self):  # wall.get
        return self._make_request(
            method="wall.get", params={"owner_id": -self.group_id}
        )['response']['items']

    def run(self):
        posts = self.get_posts()
        for post in posts:
            comments = self.get_comments(post['id'])
            for comment in comments:
                m = comment['text'].lower().strip()
                if not links_filter.review_comment(m) or not dirty_words_filter.review_message(m):
                    try:
                        self.delete_comment(comment['id'])
                    except:
                        pass


class Discussion(Api):
    def delete_comment(self, topic_id, comment_id):  # board.deleteComment
        print(self.group_id, topic_id, comment_id)
        response = self._make_request(
            method="board.deleteComment",
            params={
                "group_id": self.group_id,
                "topic_id": topic_id,
                "comment_id": comment_id,
            },
        )
        print(response)

    def get_discussions(self):  # board.getTopics
        return self._make_request(
            method="board.getTopics", params={"group_id": self.group_id}
        )['response']['items']

    def get_comments(self, topic_id):  # board.getComments
        return self._make_request(
            method="board.getComments",
            params={"group_id": self.group_id, "topic_id": topic_id},
        )['response']['items']

    def run(self):
        discussions = self.get_discussions()
        for discussion in discussions:
            comments = self.get_comments(discussion['id'])
            for comment in comments:
                m = comment['text'].lower().strip()
                if not links_filter.review_comment(m) or not dirty_words_filter.review_message(m):
                    print('yes')
                    try:
                        self.delete_comment(discussion['id'], comment['id'])
                    except Exception as e:
                        print(e)


if __name__ == '__main__':
    wall = Wall()
    discussion = Discussion()
    while True:
        wall.run()
        discussion.run()
        time.sleep(600)
