import dataclasses
import os
import json


@dataclasses.dataclass
class Trigger:
    command: str
    answer: str


def read_words() -> list[Trigger]:
    """Read file and :return actions (message_from_user: answer_from_bot) Trigger class object"""
    trigger_messages_path = "resources/trigger_messages.json"
    if not os.path.exists(trigger_messages_path):
        raise FileNotFoundError(
            "Файла с ответами триггера по пути "
            + trigger_messages_path
            + " не существует!"
        )

    try:
        triggers = json.loads(open(trigger_messages_path, "r", encoding="UTF-8").read())
    except ValueError:
        raise ValueError(
            f"В файле {trigger_messages_path} присутствует ошибка!\nИсправьте и повторите попытку!"
        )

    if type(triggers) is not dict:
        raise ValueError(
            f"Неправильный формат данных в файле {trigger_messages_path}!\nНеобходимый формат:"
            f'"Команда адресованная боту": "Ответ от бота"'
        )

    trigger_objects = []
    for trigger in triggers:
        trigger_objects.append(Trigger(trigger, triggers[trigger]))
    return trigger_objects
