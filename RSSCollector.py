import feedparser

if __name__ == '__main__':
    rss = 'http://blog.rss.naver.com/uutak2000.xml'
    feed = feedparser.parse(rss)

    for key in feed['entries']:
        title = key['title']
        publishDate = key.published
        description = key['description']
        category = key['category']
        link = key['link']
        print(title, publishDate, category)