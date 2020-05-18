from django.conf import settings
from django.shortcuts import render, redirect
import datetime
import json
import os


# Create your views here.
def index(request):
    return redirect('/news/')


def news(request, link=0):
    news_json_path = os.path.join(settings.BASE_DIR, '../', settings.NEWS_JSON_PATH)
    with open(news_json_path, 'r') as news_json_file:
        news_feed = json.load(news_json_file)
        news_dict = {}
        for news_item in news_feed:
            news_date = news_item['created'].split()
            q = request.GET.get('q')
            if q:
                if q in news_item['title']:
                    news_dict.setdefault(news_date[0], []).append(news_item)
            else:
                news_dict.setdefault(news_date[0], []).append(news_item)
            if news_item['link'] == link:
                return render(request, 'news_item.html', news_item)
        return render(request, 'news_feed.html',
                      {'news_feed': {k: news_dict[k] for k in sorted(news_dict, reverse=True)}})


def create(request):
    if request.method == 'POST':
        news_json_path = os.path.join(settings.BASE_DIR, '../', settings.NEWS_JSON_PATH)
        with open(news_json_path, 'r') as news_json_file:
            news_feed = json.load(news_json_file)
            last_link = max([item['link'] for item in news_feed])
        with open(news_json_path, 'w') as news_json_file:
            news_item = {
                'created': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'text': request.POST.get('text'),
                'title': request.POST.get('title'),
                'link': last_link + 1
            }
            news_feed.append(news_item)
            json.dump(news_feed, news_json_file)
        return redirect('/news/')
    return render(request, 'news_form.html')
