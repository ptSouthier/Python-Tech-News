from tech_news.database import find_news


def popularity_key(e):
    return e["popularity"]


def count_key(e):
    return e["count"]


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
    categories_list = []
    categories_count_list = []
    top_categories = []

    for news in find_news():
        categories_list.extend([*news["categories"]])

    for category in categories_list:
        categories_count_list.append({
            "category": category,
            "count": categories_list.count(category)
        })

    categories_count_list.sort(reverse=True, key=count_key)

    for top_category in categories_count_list:
        top_categories.append(top_category["category"])

    return sorted(top_categories)[:5]
