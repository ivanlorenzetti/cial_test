from cial_test.controler.controler import Controler

class Bot():

    def __init__(self):
        self.website = []
        file = open('website.txt', 'r')
        lines = file.readlines()
        for line in lines:
            self.website.append(line.strip())

    def run(self):
        bot = Controler(starting_urls=self.website)
        bot.scrape()


Bot().run()



