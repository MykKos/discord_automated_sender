from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import redis
from .models import Post
from django.conf import settings
# Create your views here.
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


@csrf_exempt
def add_posts(request):
    data = json.loads(request.body)
    for post_entity in data['posts']:
        post = Post()
        post.post = post_entity['post']
        post.channel = post_entity['channel']
        post.save()
        key = f"new_posts:{post.channel}:{post.id}"
        redis_instance.set(key, post.post)
    response = {
        'status': 'OK'
    }
    return JsonResponse(response)


def update_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.published = 'Y'
    post.save()
    response = {
        'status': 'OK'
    }
    return JsonResponse(response)


def ping(request):
    response = {
        'status': 'OK'
    }
    return JsonResponse(response)
