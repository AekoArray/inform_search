from crawler import Crawler

if __name__ == "__main__":
    url = 'https://kpfu.ru/'
    black_list = [".pdf"]
    crawler = Crawler(100, 1000, url, black_list)
    crawler.run()