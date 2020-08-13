import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .models import Tweet
from .forms import TweetForm

def home_view(request, *args, **kwargs):
    template = "pages/home.html"
    return render(request, template, context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next")

    if form.is_valid():
        obj = form.save(commit=False)
        obj.save() # save to db
        if request.is_ajax():
            return JsonResponse({}, status=201) # 201 == created
        if next_url and is_safe_url(next_url, allowed_hosts=settings.ALLOWED_HOSTS):
            return redirect(next_url)
        # reinitialize a new blank form here and passed back to component
        form = TweetForm()
    return render(request, 'components/form.html', context={"form": form})

def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    """
    qs = Tweet.objects.all()
    tweets_list = [
        {
            "id": x.id, 
            "content": x.content,
            "likes": random.randint(0, 10000)
        } for x in qs
    ]
    data = {
        "isUser": False,
        "response": tweets_list,
    }
    return JsonResponse(data)

def tweet_detail_view(request, *args, **kwargs):
    """
    REST API view
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