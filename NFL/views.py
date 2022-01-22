import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url


ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def NFLhome_view(request, *args, **kwargs):
    return render(request, "pages/NFLfeed.html")

def NFLtweets_list_view(request, *args, **kwargs):
    return render(request, "tweets/NFLlist.html")

def NFLtweets_detail_view(request, tweet_id, *args, **kwargs):
    return render(request, "tweets/NFLdetail.html", context={"tweet_id": tweet_id})
from django.shortcuts import render

# Create your views here.
