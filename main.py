#  Scrapes https://www.freethink.com/articles for the following datas
# - Title
# - Image link
# - News page link
# - Timestamp
# - First paragraph of the content


import requests
from bs4 import BeautifulSoup


def get_soup(url):
    # retrieves data from the site else stop the program with error message
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def main():
    results = []
    url = 'https://www.freethink.com/articles'

    main_page_soup = get_soup(url)
    loop_items = main_page_soup.find_all('div', class_='loop-item')

    # iterating over all loop-item div classes
    for loop_item in loop_items:
        # scraping main page for image link, title, news_page_link
        image_link = loop_item.find(
            'a', class_='loop-item__thumbnail-link').find('img')['src']
        title = loop_item.find(
            'a', class_='loop-item__title').text
        news_page_link = loop_item.find(
            'a', class_='loop-item__title')['href']
        # scraping news page link for timestamp and first paragraph
        news_page_soup = get_soup(news_page_link)

        time_stamp = news_page_soup.find(
            'div', class_='meta__date meta__date--published').find('time')['datetime']
        first_paragraph = news_page_soup.find('p').text

        # appending results to array
        results.append(
            {'title': title,
             'image_link': image_link,
             'news_page_link': news_page_link,
             'time_stamp': time_stamp,
             'first_paragraph': first_paragraph
             })

    print(results)

    # writing results to results.txt file
    with open('results.txt', 'w') as file:
        file.write(str(results))


if __name__ == '__main__':
    main()
