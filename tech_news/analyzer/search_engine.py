from tech_news.database import search_news
from datetime import datetime


# Requisito 6
def search_by_title(title):
    news_list = []
    for news in search_news({"title": {"$regex": title, "$options": "i"}}):
        news_list.append((news["title"], news["url"]))

    return news_list


# Requisito 7
def search_by_date(date):
    news_list = []
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")

    for news in search_news({"timestamp": {"$regex": date}}):
        news_list.append((news["title"], news["url"]))

    return news_list


# Requisito 8
def search_by_source(source):
    news_list = []
    for news in search_news({"sources": {"$regex": source, "$options": "i"}}):
        news_list.append((news["title"], news["url"]))

    return news_list


# Requisito 9
def search_by_category(category):
    news_list = []
    for news in search_news(
        {"categories": {"$regex": category, "$options": "i"}}
    ):
        news_list.append((news["title"], news["url"]))

    return news_list
