import feedparser


def parse(feed):
    return feedparser.parse(feed)


def get_headlines(url, number=3):
    headlines = []
    feed = parse(url)
    print("Articles from: {}".format(feed['feed']['title']))
    for newsitem in feed['items'][0:number]:
        headlines.append("*{}* {}".format(newsitem['title'], newsitem['link']))
    return headlines


if __name__ == "__main__":
    for h in get_headlines('http://tceprincipalnews.blogspot.com/feeds/posts/default'):
        print(h)
