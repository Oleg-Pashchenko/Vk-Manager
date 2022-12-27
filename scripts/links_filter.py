import os


def read_links() -> set:
    """Read file and :return allowed resources in set"""
    allowed_resources_path = "../resources/allowed-resources_links.txt"
    if not os.path.exists(allowed_resources_path):
        raise FileNotFoundError(
            "Файла с разрешенными ссылками по пути "
            + allowed_resources_path
            + " не существует!"
        )
    file = open(allowed_resources_path, "r", encoding="UTF-8")
    return set(file.read().split("\n"))


def get_links_from_comment(message: str) -> set[str]:
    """returns all links from comment"""
    links = set()
    message = message.split()
    for word in message:
        if "https://" in word or "http://" in word:
            links.add(word)
    return links


def review_comment(message: str) -> bool:
    """returns false result if not allowed link(s) in comment or true if not"""
    allowed_links = read_links()
    links_from_comment = get_links_from_comment(message)
    for link in links_from_comment:
        if link not in allowed_links:
            return False
    return True
