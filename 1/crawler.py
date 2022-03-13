import requests
import bs4
from urllib.parse import urlparse
import json
from langdetect import detect
import cld2

class Crawler:
    def __init__(self, number_of_pages, number_of_words, start_url, black_list):
        self.number_of_pages = number_of_pages
        self.number_of_words = number_of_words
        self.start_url = start_url
        self.visited_urls = []
        self.all_href: list = []
        self.black_list = black_list

    def clear_HTML(self, html):
        soup = bs4.BeautifulSoup(html, 'html.parser').text
        string = ' '.join(soup.split())
        return string

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def get_len(self, str):
        opt = str.split(" ")
        return len(opt)

    def get_hrefs(self, request):
        urls = []
        soup = bs4.BeautifulSoup(request.content, "html.parser")
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue
            if href in urls:
                continue
            if href in self.all_href:
                continue
            if self.is_valid_url(href):
                urls.append(href)
        return urls

    def run(self):
        if self.is_valid_url(self.start_url):
            self.all_href.append(self.start_url)
            self.visited_urls.append(self.start_url)
            page_number = 0
            counter = 0

            urls = []

            while page_number < self.number_of_pages:
                current_page = self.all_href[counter]
                print(f"Current page: {current_page}")
                try:
                    if self.is_valid_url(current_page) and current_page is not None and not any(
                            x in current_page for x in self.black_list):
                        request = requests.get(current_page)
                        self.all_href += self.get_hrefs(request)
                        text = self.clear_HTML(request.text)
                        length = self.get_len(text)
                        details = cld2.detect(text)
                        if length >= self.number_of_words and details.details[0].percent >= 95 and details.details[0].language_name == 'RUSSIAN':
                            page_number += 1
                            counter += 1
                            self.visited_urls.append(current_page)
                            file = open(f"files2/{page_number}.txt", 'wb')
                            file.write(text.encode("utf-8"))
                            urls.append({"url": current_page, "file_name": f"{page_number}.txt"})
                        else:
                            counter += 1
                    else:
                        counter += 1
                        continue
                except Exception as e:
                    print("connection error")
                    print(e)
                    counter += 1
            hrefs = open('index2.txt', 'w', errors="ignore")
            hrefs.write(json.dumps(urls, indent=4, sort_keys=True))
