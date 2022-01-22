import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url


ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def Worldcuphome_view(request, *args, **kwargs):
    return render(request, "pages/Worldcupfeed.html")

def Worldcuptweets_list_view(request, *args, **kwargs):
    return render(request, "tweets/Worldcuplist.html")

def Worldcuptweets_detail_view(request, tweet_id, *args, **kwargs):
    return render(request, "tweets/Worldcupdetail.html", context={"tweet_id": tweet_id})
from django.shortcuts import render

# Create your views here.
