from urllib.request import urlopen
from urllib.parse import urlparse
import re

REGEX_LINK = re.compile("<a [^>]*href=['\"]([^'\"]+)['\"][^>]*>")

url = "http://192.168.1.22:8000"
# url = "https://vietnamnet.vn"


class UrlCrawling:
    def __init__(self, url):
        self.url = url
        self.collected_links = set()
        self.visited_links = set()

    def get_collection(self):

        self.visited_links.add(self.url)
        print(self.visited_links)

        pages = urlopen(self.url).read()
        self.links = REGEX_LINK.findall(str(pages))

        new_links = [self.normalize_url("/",i) for i in self.links]

        set_links = set(new_links)
        # self.visited_links.add(set_links)

        unvisited_links = set_links.difference(self.visited_links)
        list_links = list(set_links)

    def normalize_url(self, path, link):
        if link.startswith("http://"):
            return link
        elif link.startswith("/"):
            return self.url + link
        else:
            return self.url + path.rpartition('/')[0] + '/' + link

    def save_collection(self):
        new_links = self.get_collection()
        with open("links_page.txt", "w") as f:
            for link in new_links:
                f.write(f"{link}\n")


# do_url_crawling = UrlCrawling(url)
# do_url_crawling.save_collection()

get_crawling = UrlCrawling(url)
get_crawling.save_collection()
