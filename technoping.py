#!/usr/bin/env python

__author__ = "Luke Hoersten"
__email__ = "Luke@Hoersten.org"
__website__ = "http://Luke.Hoersten.org"
__version__ = "0.2"
__copyright__ = "Copyright (C) 2008, Luke Hoersten"

__license__ = """
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
"""

__doc__ = """
Ping Technorati.com with SOURCE pages which link to TARGET.  The
target is usually your page and the sources are pages which link to
yours.
"""

__deps__ = """
feedparser (http://www.feedparser.org/),

"""

__TODO__ = """
1. check for feeds in souce page to make sure technorati will count it
2. add sources (http://www.joostdevalk.nl/find-out-whos-scraping-you/)
3. add Mint source (http://www.joostdevalk.nl/mint/?RSS=c257ed97645559f061a798adba7b4ec5&pepper=0)
4. parallelise technorati pinging
5. parallelise parsing of each source
6. Google Blog Search for last 24 hours or 100 links. Link count variable.
7. add sqlite backend so no URL is pinged twice.
"""

import sources
from optparse import OptionParser
from urllib2 import urlopen

def main():
    usage = "Usage: %prog [OPTIONS] TARGET_URL" # Lazy: target is required
    version = "%%prog %s\n%s %s" % (__version__,  __copyright__,  __license__)
    parser = OptionParser(usage=usage, version=version)

    parser.add_option("--google-blog-off",
                      action="store_false", dest="google_blog", default=True,
                      help="don't use Google Blog Search as a source")
    parser.add_option("--wasa-off",
                      action="store_false", dest="wasa", default=True,
                      help="don't use Wasa Live as a source")

    parser.add_option("-m", "--mint", dest="mint_url",
                      help="use Mint stats FEED as a source", metavar="FEED")
    parser.add_option("-w", "--google-web-tools", dest="google_web_tools",
                      help="use a Google Webmaster Tools comma separated value FILE as a source", metavar="FILE")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        exit(1)

    target_url = args[0]
    hostnames = []

    if options.google_blog:
        source = sources.GoogleBlogSearch()
        links = source.links(target_url) # OPT: cache this
        if options.verbose: print "%s found %d sources." % (source.name(), len(links))
        hostnames += links

    if options.wasa:
        source = sources.WasaLive()
        links = source.links(target_url) # OPT: cache this
        if options.verbose: print "%s found %d sources." % (source.name(), len(links))
        hostnames += links

    if options.google_web_tools:
        source = sources.GoogleWebmasterTools()
        links = source.links(options.google_web_tools)
        if options.verbose: print "%s found %d sources." % (source.name(), len(links))
        hostnames += links

    print "\nPinging..."
    print hostnames
#    ping(set(hostnames), options.verbose) # Unique with set() # OPT: parallelize pinging



def ping(hostnames, verbose):
    PING_URL = "http://technorati.com/ping?url=%s"
    num_hostnames = len(hostnames)

    if verbose:
        print "Pinging Technorati with %d incoming links...\n" % num_hostnames

    for hostname in hostnames:
        print "Pinging %s..." % hostname
        urlopen(PING_URL % hostname)

    if verbose:
        print "\nPinged Technorati with %d incoming links." % num_hostnames



if __name__ == "__main__":
    main()
