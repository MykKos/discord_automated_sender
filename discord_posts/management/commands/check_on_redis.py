import time
import redis
from django.core.management import BaseCommand
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Waiting for Redis...')
        redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                           port=settings.REDIS_PORT, db=0)
        while True:
            try:
                redis_instance.ping()
                break
            except Exception:
                self.stdout.write('Redis unavailable, waititng 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Redis available!'))
