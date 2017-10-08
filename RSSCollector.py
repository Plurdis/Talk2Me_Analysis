import feedparser
import BaseCollector

class RSSCollector(BaseCollector.BaseCollector):
    def __init__(self, url):
        super(RSSCollector, self).__init__()
        self.url = url

    def printTest(self):
        feed = feedparser.parse(self.url)

        for key in feed['entries']:
            title = key['title']
            publishDate = key.published
            description = key['description']
            category = key['category']
            link = key['link']
            print(title, publishDate, category)

if __name__== '__main__':
    rc = RSSCollector('http://blog.rss.naver.com/uutak2000.xml')
    rc.printTest()