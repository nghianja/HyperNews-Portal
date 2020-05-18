from django.conf import settings
from django.shortcuts import render
import json


# Create your views here.
def index(request):
    return render(request, 'index.html')


def news(request, link):
    context = {}
    with open(settings.NEWS_JSON_PATH, 'r') as news_json_file:
        news_feed = json.load(news_json_file)
        for news_item in news_feed:
            if news_item['link'] == link:
                context = news_item
                break
    return render(request, 'news_item.html', context)
