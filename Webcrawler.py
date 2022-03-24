from bs4 import BeautifulSoup
import urllib


class WebCrawler:
    def __init__(self, url):
        self.url = url
        self.soup = 0
        self.page_text = ""
        self.page_title = ""

    def getPageSoup(self):
        request_url = urllib.request.urlopen(self.url)
        page = request_url.read().decode()
        soup = BeautifulSoup(page, 'html.parser')
        self.soup = soup
    
    def getPageText(self):
        page_text = self.soup.find_all('p')
        page_string = ""
        for p in page_text:
            page_string += p.get_text()
        self.page_tsxt = page_string

    def getPageTitle(soup):
        self.page_title = self.soup.title.string