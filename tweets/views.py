from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Tweet

def home_view(request,*args, **kwargs):
    return HttpResponse("<h1>Hello World</h1>")


def tweet_detail_view(request, *args, **kwargs):
    """
    REST API view
    Consume by JS or Swift/Java/iOS/Android
    return JsonResponse
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