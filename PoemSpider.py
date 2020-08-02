import requests
from random import randint
from lxml import etree
import re
from PyQt5.QtCore import *


class PoemThread(QThread):
    poem_signal = pyqtSignal(str)
    headers = {
        'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
    width = 15

    def __init__(self):
        super().__init__()

    def run(self):
        poem_id = randint(1, 9598)

        response = requests.get(f"http://www.yemeishequ.com/gusiwen/detail_{poem_id}.html",
                                headers=self.headers)

        text = response.content.decode('utf-8')

        html = etree.HTML(text)

        title = html.xpath("//h1/text()")[0]

        author = html.xpath("//div[@class='sons'][1]//p[@class='source']//text()")
        author = ''.join(author).strip()

        article = html.xpath("//div[@class='sons'][1]//div[@class='contson']//text()")
        article = re.sub(r'[\x20]', '', ''.join(article).strip())


        space = ' ' * (self.width - len(title))
        poem = space + title + '\n              ' + author + '\n\n' + article

        self.poem_signal.emit(poem)
