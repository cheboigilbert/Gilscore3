import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from ..forms import TweetForm
from ..models import Tweet, Comment
from ..serializers import (
    TweetSerializer, 
    TweetActionSerializer,
    CommentActionSerializer,
    TweetCreateSerializer,
    CommentCreateSerializer,
    CommentSerializer
)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

@api_view(['POST']) # http method the client == POST
# @authentication_classes([SessionAuthentication, MyCustomAuth])
@permission_classes([IsAuthenticated]) # REST API course
@parser_classes ([MultiPartParser, JSONParser])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['POST']) # http method the client == POST
# @authentication_classes([SessionAuthentication, MyCustomAuth])
@permission_classes([IsAuthenticated]) # REST API course
@parser_classes ([MultiPartParser, FormParser, JSONParser])
def comment_create_view(request, *args, **kwargs):
    serializer = CommentCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
@parser_classes ([MultiPartParser,JSONParser])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['GET'])
@parser_classes ([MultiPartParser, FormParser, JSONParser])
def comment_detail_view(request, comment_id, *args, **kwargs):
    qs = Comment.objects.filter(id=comment_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = CommentSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@parser_classes ([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet removed"}, status=200)

@api_view(['DELETE', 'POST'])
@parser_classes ([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def comment_delete_view(request, comment_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=comment_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this comment"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Comment removed"}, status=200)

@api_view(['POST'])
@parser_classes ([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, retweet
    '''
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(
                    user=request.user, 
                    parent=obj,
                    content=content,
                    )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
    return Response({}, status=200)

@api_view(['POST'])
@parser_classes ([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def comment_action_view(request,*args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, retweet
    '''
    serializer = CommentActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        comment_id = data.get("id")
        action = data.get("action")
        content =data.get("content")
        image = data.get("image")
        qs = Comment.objects.filter(id=comment_id)
        if not qs.exists():
            return Response({},  status = 404)
        obj = qs.first()
        if action =="like":
            obj.likes.add(request.user)
            serializer = CommentSerializer(obj)

        elif action =="unlike":
            obj.likes.remove(request.user)
            serializer = CommentSerializer(obj)
        elif action == "retweet":
            new_comment = Comment.objects.create(
                      user=request.user,
                      parent=obj,
                      content=content,

                      )
            serializer = CommentSerializer(new_comment)
            return Response(serializer.data, status=201)
    return Response({}, status=200)



def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_qs = paginator.paginate_queryset(qs, request)
    serializer = TweetSerializer(paginated_qs, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data) # Response( serializer.data, status=200)

def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_qs = paginator.paginate_queryset(qs, request)
    serializer = CommentSerializer(paginated_qs, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data) # Response( serializer.data, status=200)


@api_view(['GET'])
@parser_classes ([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def tweet_feed_view(request, *args, **kwargs):
    user = request.user
    qs = Tweet.objects.feed(user)
    return get_paginated_queryset_response(qs, request)


@api_view(['GET'])
@parser_classes ([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def comment_feed_view(request, *args, **kwargs):
    qs = Comment.objects.all()
    username = request.GET.get('username') # ?username=Justin
    if username != None:
        qs = qs.by_username(username)
    return get_paginated_queryset_response(qs, request)

@api_view(['GET'])
@parser_classes ([MultiPartParser, FormParser,JSONParser])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    username = request.GET.get('username') # ?username=Justin
    if username != None:
        qs = qs.by_username(username)
    return get_paginated_queryset_response(qs, request)



def tweet_create_view_pure_django(request, *args, **kwargs):
    '''
    REST API Create View -> DRF
    '''
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        # do other form related logic
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 == created items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})


def tweet_list_view_pure_django(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Andriod
    return json data
    """
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Andriod
    return json data
    """
    data = {
        "id": tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
    return JsonResponse(data, status=status) # json.dumps content_type='application/json'