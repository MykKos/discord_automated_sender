import requests
import time
import redis
import json
import os


def process_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return False
    return wrapper


class DiscordInteractor:

    def __init__(self, token, bot_token=None):
        self.auth = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        self.api = 'https://discord.com/api/v8'
        self.redis = redis.StrictRedis(host=os.environ.get('REDIS_HOST'),
                                       port=os.environ.get('REDIS_PORT'), db=0)

    @process_errors
    def discord_request(self, content: object, channel: str):
        timeout = -1
        webhook = self.channel_webhook(channel)
        while timeout != 0:
            send_url = f"{self.api}/webhooks/{webhook}"
            r = requests.post(send_url,
                              headers=self.auth, json=content)
            headers = r.headers
            try:
                rl = int(headers['X-RateLimit-Remaining'])
                rs = float(headers['X-RateLimit-Reset']) + 3
            except Exception:
                if '"code": 50035' in r.text:
                    for i, embed in enumerate(content['embeds']):
                        embed.pop('image', None)
                        if 'description' not in embed:
                            content['embeds'].pop(i)
                    rl = 1
            if rl == 0:
                timeout = rs - time.time()
            else:
                timeout = 0
            if timeout < 0:
                timeout = 0
            time.sleep(timeout)
            if r.text == '':
                timeout = 0
            if '"code": 50035' in r.text:
                timeout = 1
        return True

    def channel_webhook(self, channel: str) -> str:
        wh = self.redis.get(f"webhooks:{channel}")
        if wh is None:
            wh_url = f"{self.api}/channels/{channel}/webhooks"
            r = requests.get(wh_url, headers=self.auth)
            webhooks = json.loads(r.text)
            if len(webhooks) != 0:
                wh = webhooks[0]
            else:
                wh = self.create_webhook(channel)
            wh = f"{wh['id']}/{wh['token']}"
            self.redis.set(f"webhooks:{channel}", wh)
        else:
            wh = wh.decode('utf-8')
        return wh

    def create_webhook(self, channel: str) -> str:
        wh_url = f"{self.api}/channels/{channel}/webhooks"
        author = {
            'name': 'default'
        }
        r = requests.post(wh_url, json=author, headers=self.auth)
        return json.loads(r.text)
