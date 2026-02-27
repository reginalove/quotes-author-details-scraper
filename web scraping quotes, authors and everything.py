import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

url = "https://quotes.toscrape.com/"

all_data = []

while True:

    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html.parser')

    each_html = soup.find_all('div', class_='quote')

    for each_quote in each_html:
        quotes = each_quote.find('span', class_='text').text
        author = each_quote.find('small', class_='author').text
        tags = each_quote.find_all('a', class_='tag')
        about_ = each_quote.find('small', class_ = "author").find_next_sibling("a")['href']

        tag_list = []

        for tag in tags:
            tag_list.append(tag.text)

        print(quotes)
        print(author)
        print(tag_list)

        url_author = urljoin(url, about_)
        request_author = requests.get(url_author)
        soup_author = BeautifulSoup(request_author.content, 'html.parser')

        date_Author = soup_author.find('span', class_='author-born-date').text
        location_author = soup_author.find('span', class_='author-location').text

        print(author, "Born in: ", date_Author)
        print(author, "Location is in: ", location_author)

        all_data.append({
            "quotes": quotes,
            "author": author,
            "tags": tag_list,
            "author's date": date_Author,
            "author's location": location_author,
        })



    next_page = soup.find('li', class_='next')
    if not next_page:
        break
    next_url = next_page.find("a")['href']
    url = urljoin(url, next_url)

with open("all_quotes.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False)
