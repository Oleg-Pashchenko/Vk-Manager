import json
import random

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from scripts import links_filter, dirty_words_filter, trigger_actions


tokens = json.loads(open("secrets.json", "r").read())
vk_session = vk_api.VkApi(token=tokens["group_token"])
longpoll = VkBotLongPoll(vk_session, "197992580")
vk = vk_session.get_api()
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.obj['message']['peer_id'] >= 2000000000:
            m = event.obj["message"]["text"].lower().strip()
            if not links_filter.review_comment(m) or not dirty_words_filter.review_message(m):
                try:
                    vk.messages.delete(
                        peer_id=event.obj["message"]["peer_id"],
                        delete_for_all=1,
                        cmids=event.obj["message"]["conversation_message_id"],
                    )
                except:
                    pass
        else:
            triggers = trigger_actions.read_words()
            m = event.obj["message"]["text"].lower().strip()
            for trigger in triggers:
                if trigger.command.lower() == m:
                    vk.messages.send(
                        user_id=event.object['message']['from_id'],
                        message=trigger.answer,
                        random_id=random.randint(10000000, 100000000)
                    )
