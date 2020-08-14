import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer


def home_view(request, *args, **kwargs):
    """
    Home page that hosts the JS / React
    """
    template = "pages/home.html"
    return render(request, template, context={}, status=200)


@api_view(['POST']) # http method client needs to be post
# @authentication_classes([SessionAuthentication]) # only session authentication is a valid source of auth
@permission_classes([IsAuthenticated]) # only allow access to this view if authenticated
def tweet_create_view(request, *args, **kwargs):
    """
    REST API Create View with Django Rest Framework
    """
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


def tweet_create_view_pure_django(request, *args, **kwargs):
    """
    BACKUP VIEW
    """
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401) #not authorized
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next")

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save() # save to db
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 == created
        if next_url and is_safe_url(next_url, allowed_hosts=settings.ALLOWED_HOSTS):
            return redirect(next_url)
        # reinitialize a new blank form here and passed back to component
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW using DRF
    """
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)


def tweet_list_view_pure_django(request, *args, **kwargs):
    """
    REST API VIEW in Pure Django
    """
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list,
    }
    return JsonResponse(data)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW using DRF
    """
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data)


def tweet_detail_view_pure_django(request, *args, **kwargs):
    """
    REST API view in pure django
    """
    tweet_id = kwargs.get('tweet_id')
    data = {"id": tweet_id,}
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content,
        # datap"image_path"] = obj.image.url,
        status = 200
    except:
        data['message'] = "Not found"
        status = 404

    return JsonResponse(data, status=status) # json.dumps content_type='application/json'