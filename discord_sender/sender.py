from discord_interactor import DiscordInteractor
from threading import Thread
from queue import Queue
import redis
import os
import json
import time


def loop(func):
    def wrapper(*a, **b):
        while True:
            func(*a, **b)

    return wrapper


class Sender:

    def __init__(self, d_token,
                 b_token=None
                 ):
        self.redis = redis.StrictRedis(host=os.environ.get('REDIS_HOST'),
                                       port=os.environ.get('REDIS_PORT'), db=0)
        while True:
            try:
                self.redis.ping()
                break
            except Exception:
                print('Redis unavailable!')
                time.sleep(1)
        self.ds = DiscordInteractor(d_token, bot_token=b_token)
        self.queues = {}
        self.without_thread = []

    def run(self):
        fill_thread = Thread(target=self.fill_queues, args=[])
        send_thread = Thread(target=self.send_from_queues, args=[])
        fill_thread.start()
        send_thread.start()

    @loop
    def fill_queues(self):
        new_messages = self.redis.keys('new_posts:*')
        for message in new_messages:
            message_utf8 = message.decode('utf-8')
            channel = message_utf8.split(':')[1]
            if channel not in self.queues or self.queues[channel].qsize() == 0:
                print('Filling queue....')
                self.add_to_queue(message)

    def add_to_queue(self, message: str):
        message_utf8 = message.decode('utf-8')
        p, channel, post_id = message_utf8.split(':')
        post = self.redis.get(message)
        if channel not in self.queues:
            self.queues[channel] = Queue()
            self.without_thread.append(channel)
        proc_key = f"processed:{channel}:{post_id}"
        self.delete_from_queue(message)
        self.add_to_redis(proc_key, post)
        self.queues[channel].put((proc_key, post_id, post))

    @loop
    def send_from_queues(self):
        threads = []
        for q in self.without_thread:
            threads.append(Thread(target=self.send_from_queue,
                                  args=[self.queues[q], q]
                                  )
                           )
            self.without_thread.remove(q)
        for t in threads:
            t.start()

    @loop
    def send_from_queue(self, queue: Queue, channel: str):
        queue_element = queue.get()
        post_string = queue_element[2].decode('utf-8')
        post = json.loads(post_string)
        for message in post:
            self.ds.discord_request(message, channel)
        self.sent_back(queue_element[1])
        self.delete_from_queue(queue_element[0])
        print('Success!')

    def sent_back(self, post_id: str):
        self.redis.rpush("sent_messages", post_id)

    def delete_from_queue(self, key: str):
        self.redis.delete(key)

    def add_to_redis(self, key: str, value: str):
        self.redis.set(key, value)


if __name__ == '__main__':
    sender = Sender(os.environ.get('DISCORD_USER_AUTH'))
    sender.run()
