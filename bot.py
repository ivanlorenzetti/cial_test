from cial_test.controler.controler import Controler
import sys


class Bot():

    def __init__(self):
        self.stdin_txt_file = None
        self.websites = []

        if sys.stdin.isatty():
            sys.exit('How to use: cat website.txt | python3 bot.py ')

        self.stdin_txt_file = sys.stdin

        for x in self.stdin_txt_file:
            self.websites.append(x.strip())

    def run(self):
        bot = Controler(starting_urls=self.website)
        bot.scrape()

Bot().run()

