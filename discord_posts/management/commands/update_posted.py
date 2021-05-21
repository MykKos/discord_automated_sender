import redis
from django.core.management import BaseCommand
from django.conf import settings
from discord_posts.models import Post
import time


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Waiting for Redis...')
        redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                           port=settings.REDIS_PORT, db=0)
        while True:
            update = redis_instance.lpop('sent_messages')
            try:
                post = Post.objects.get(pk=update)
                post.published = 'Y'
                post.save()
                print('Something updated')
            except Exception:
                continue
            print('Iteration')
            time.sleep(1)
