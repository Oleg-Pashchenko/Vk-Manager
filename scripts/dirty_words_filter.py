import os


def read_words() -> set:
    """Read file and :return dirty words in set"""
    dirty_words_path = '../resources/dirty-words.txt'
    if not os.path.exists(dirty_words_path):
        raise FileNotFoundError("Файла с матом по пути " + dirty_words_path + " не существует!")
    file = open(dirty_words_path, 'r', encoding='UTF-8')
    return set(file.read().split('\n'))


def review_message(message: str) -> bool:
    """returns false result if banned words in message or true if not"""
    banned_words = read_words()
    for word in banned_words:
        if word in message:
            return False
    return True

