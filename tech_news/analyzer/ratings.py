from tech_news.database import find_news


def popularity_key(e):
    return e["popularity"]


# Requisito 10
def top_5_news():
    news_dict_list = []
    top_news_list = []
    for news in find_news():
        news_dict_list.append({
            "title": news["title"],
            "url": news["url"],
            "popularity": (news["shares_count"] + news["comments_count"])
        })

    news_dict_list.sort(reverse=True, key=popularity_key)

    for top_news in news_dict_list:
        top_news_list.append((top_news["title"], top_news["url"]))

    return top_news_list[:5]


# Requisito 11
def top_5_categories():
    """Seu código deve vir aqui"""
