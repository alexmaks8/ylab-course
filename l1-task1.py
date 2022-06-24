'''
Задача №1. Секция статьи "Задача №1."
Написать метод domain_name, который вернет домен из url адреса:
'''

import re

def domain_name(url):
    if re.search(r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/\.]+)", url):
        domain = re.findall(r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/\.]+)", url)
        dom = "".join(domain)
        return dom

if __name__ == '__main__':
    assert domain_name("http://google.com") == "google"
    assert domain_name("http://google.co.jp") == "google"
    assert domain_name("www.xakep.ru") == "xakep"
    assert domain_name("https://youtube.com") == "youtube"

