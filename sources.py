import csv # for Google Webmaster Tools
import feedparser # for RSS like Google Blog Search
from urlparse import urlparse

class Csv:
    pass



class Feed:
    """
    Parse feeds for source links.
    """

    def hostname(self, url):
        url = urlparse(url)
        return url.hostname if url.scheme else url.path

    def parse(self, feed_entry):
        return (urlparse(feed_entry.link)).hostname



class GoogleWebmasterTools(Csv):
    """
    Google Webmaster Tools (http://www.google.com/webmasters/tools/)
    comma separated values parser.
    """

    def name(self):
        return "Google Webmaster Tools"

    def links(self, csv_file):
        reader = csv.reader(open(csv_file, "rb"))
        reader.next() # read past header
        return [parse(csv_row) for csv_row in reader]

    def parse(self, csv_row):
        CSV_URL_COLUMN = 1 # URL column number in table
        return (urlparse(csv_row[self.CSV_URL_COLUMN])).hostname



class GoogleBlogSearch(Feed):
    """
    Google Blog Search (http://blogsearch.google.com/) feed parser.
    """

    def name(self):
        return "Google Blog Search"

    def links(self, target_url):
        RANGE = {'month': "m", 'day': "d",'alltime': "a"}
        FEED_URL = "http://blogsearch.google.com/blogsearch_feeds?as_q=\
link:%(target_hostname)s&hl=en&c2coff=1&as_epq=&as_oq=&as_eq=&as_drrb=q&as_qdr=\
%(range)s&lr=&safe=off&q=link:%(target_hostname)s&ie=utf-8&num=%(num_results)d&\
output=rss"
        # These can be tweeked later to maximize database hits
        feed_url = FEED_URL % { 'target_hostname': self.hostname(target_url),
                                'range': RANGE['alltime'],
                                'num_results': 100 }
        feed = feedparser.parse(feed_url)
        return [self.parse(entry) for entry in feed.entries]



class WasaLive(Feed):
    """
    WasaLive (http://en.wasalive.com/) feed parser.
    """

    def name(self):
        return "Wasa Live"

    def links(self, target_url):
        FEED_URL = "http://en.wasalive.com/rss/en/%s"
        feed_url = FEED_URL % self.hostname(target_url)
        feed = feedparser.parse(feed_url)
        return [self.parse(entry) for entry in feed.entries]



class Mint(Feed):
    """
    Mint (http://haveamint.com/) feed parser. This requires your secret
    feed.
    """

    def name(self):
        return "Mint"

    def links(self, feed_url):
        feed = feedparser.parse(feed_url)
        return [self.parse(entry) for entry in feed.entries]
