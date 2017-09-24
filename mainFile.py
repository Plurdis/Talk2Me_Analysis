import feedparser

class RSSReader:
    def Read(url):
        d = feedparser.parse(url)
        # print(d['channel']['description'])
        for x in d.entries[0]:
            print(x.get('title',''))
            print(x.get('summary',''))



RSSReader.Read("http://blog.rss.naver.com/uutak2000.xml")

# for x in range(5):
#     print('*' * (x + 1))

#d = feedparser.parse('http://wptavern.com/feed');

#for post in d.entries:
#    print(post.title + ":" + post.link + '\n');
