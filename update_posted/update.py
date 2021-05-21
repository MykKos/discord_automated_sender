import redis
import requests
import time
import os


def loop(func):
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)
    return wrapper


@loop
def updated(redis_instance):
    update = redis_instance.lpop('sent_messages')
    if update is not None:
        update = update.decode('utf-8')
        # try:
        requests.get(f"http://poster:8000/posts/update/{update}")
        print('Something updated')
        # except Exception:
        #     pass
    print('Iteration')
    time.sleep(1)


if __name__ == '__main__':
    redis_instance = redis.StrictRedis(host=os.environ.get('REDIS_HOST'),
                                       port=os.environ.get('REDIS_PORT'), db=0)
    while True:
        try:
            redis_instance.ping()
            break
        except Exception:
            print('Redis unavailable!')
            time.sleep(1)
    while True:
        try:
            requests.get("http://poster:8000/posts/ping")
            print('Django is ready')
            break
        except Exception:
            print('Django is not ready')
            time.sleep(1)
    updated(redis_instance)
