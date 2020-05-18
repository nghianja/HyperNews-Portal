from django.conf import settings
from django.shortcuts import render
import json
import os


# Create your views here.
def index(request):
    return render(request, 'index.html')


def news(request, link=0):
    news_json_path = os.path.join(settings.BASE_DIR, '../', settings.NEWS_JSON_PATH)
    with open(news_json_path, 'r') as news_json_file:
        news_feed = json.load(news_json_file)
        news_dict = {}
        for news_item in news_feed:
            news_date = news_item['created'].split()
            news_dict.setdefault(news_date[0], []).append(news_item)
            if news_item['link'] == link:
                return render(request, 'news_item.html', news_item)
        return render(request, 'news_feed.html',
                      {'news_feed': {k: news_dict[k] for k in sorted(news_dict, reverse=True)}})
