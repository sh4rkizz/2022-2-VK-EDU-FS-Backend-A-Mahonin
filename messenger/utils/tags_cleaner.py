from bs4 import BeautifulSoup


def clear_tags(message):
    clear_text = BeautifulSoup(message, 'html.parser')

    return clear_text.get_text()
