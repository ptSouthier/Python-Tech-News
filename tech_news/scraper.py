import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        if response.status_code != 200:
            return None
        return response.text
    except requests.Timeout:
        return None


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    news_list = selector.css(".tec--card__info h3 a::attr(href)").getall()
    return news_list


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next_page_url = selector.css(".tec--btn--lg::attr(href)").get()
    return next_page_url


def get_writer(selector):
    writer = selector.css(".tec--author__info p:first-child *::text").get()

    if writer is None:
        writer = selector.css(".tec--timestamp__item a::text").get()

    return writer


# Requisito 4
def scrape_noticia(html_content):
    selector = Selector(text=html_content)

    url = selector.xpath("//link[contains(@rel, 'canonical')]/@href").get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css(".tec--timestamp time::attr(datetime)").get()
    writer = get_writer(selector)
    shares_count = selector.css(".tec--toolbar__item::text").get()
    comments_count = selector.css("#js-comments-btn::attr(data-count)").get()
    summary_array = selector.css(
        ".tec--article__body p:first-child *::text"
    ).getall()
    summary = "".join(summary_array)

    sources = []
    for source in selector.css(".z--mb-16 div a::text").getall():
        sources.append(source.strip())
    categories = []
    for category in selector.css("#js-categories a::text").getall():
        categories.append(category.strip())

    if writer is not None:
        writer = writer.strip()

    if shares_count is None:
        shares_count = 0
    else:
        shares_count = shares_count[1:3]

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": int(shares_count),
        "comments_count": int(comments_count),
        "summary": summary,
        "sources": sources,
        "categories": categories,
    }


# Requisito 5
def get_tech_news(amount):
    url = "https://www.tecmundo.com.br/novidades"
    html_content = fetch(url)
    news_list = []
    last_n_news = scrape_novidades(html_content)

    while len(last_n_news) < amount:
        next_page_url = scrape_next_page_link(html_content)
        next_page_content = fetch(next_page_url)
        for news in scrape_novidades(next_page_content):
            last_n_news.append(news)

    for news_url in last_n_news[:amount]:
        news_content = fetch(news_url)
        news_list.append(scrape_noticia(news_content))

    create_news(news_list)
    return news_list
