from lxml import html
import requests

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

def scraper(web):
    response = requests.get(web, headers=header)
    dom = html.fromstring(response.text)
    items = dom.xpath("//p[contains(@class, 'topic-body__content')]/text()")
    return [''.join(items)]

# text = scraper('https://lenta.ru/news/2022/04/21/marrrrr/')
# print(text)