# Fully automated, server-based Discord posting service

### What is it used for?

You can start it on your server and send messages to it then they will be posted to the chosen channel.
It can be an interface, some scripts for processing and passing data, automated tools duplicating data from different sources, etc.
As one example usages, you can build an interface, where the user will build the message in the simple editor and then send the result to the server([example of interface](https://leovoel.github.io/embed-visualizer/))


### How is it works?

You should pass all post objects with channels where they need to send as an array.
Each post can have an unlimited amount of messages.
Message object detailed [here](https://discord.com/developers/docs/resources/channel#create-message).

```json
{
    "posts":[
        {
            "post": "[
              {\"content\":\"Message #1\"},
              {\"content\":\"Message #2\"},
              {\"content\":\"Message #3\"},
            ]",
            "channel": "845194299906064415"
        }
    ]
}
```

Endpoint for that is: `http://your-server-ip:8000/posts/add`

### How to start?

Fill `docker-compose.yml` with data you wish:

1. In `db` service put the database authorization data(could be any).

2. In `poster` service put the database authorization data from the previous step.

3. In `discord` service put your authorization token from Discord.
   - Later will be added an opportunity to use your login-password.

Also, you can change Redis port/host, if it needs.
