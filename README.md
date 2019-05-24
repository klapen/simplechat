# Siemple Chat

Simple chat using [Python Channels](https://channels.readthedocs.io/en/latest/tutorial/part_1.html) and [Celery](http://docs.celeryproject.org/en/latest/index.html)

# Before you start

The project uses [redis](https://redis.io/) as broker for the messages. Before running the server you should start a redis server, it can be done easily with [docker]():

```sh
$ docker run -p 6379:6379 redis:2.8
```

After that 

# Start server

First of all, clone the repository, install requirements and initialize the database:

```sh
$ git clone https://github.com/klapen/simplechat.git
$ cd simplechat/src
$ pip install requirements.txt
$ python3 manage.py loaddata fixtures/users
```

Loaddata command will load 3 users to test:

| Username  | Password | Role  |
|-----------|----------|-------|
| admin     | 12345    | admin |
| usertest1 | us112345 | user  |
| usertest2 | us212345 | user  |

Second of all start the chat server:

```sh
$ cd simplechat/src
$ python manage.py migrate
$ python manage.py runserver
```

And finally, start the message queue workers:

```sh
$ cd simplechart/src
$ celery -A simplechat worker -l info
```

# How to use

Open on a web browser a [login page](http://127.0.0.1:8000/login/) and enter a valid username and password. It will redirect you to the chat room creating page.

Enter a chat room name and press enter and you are now able to send messages.

If you want to use the stock quote bot, send a the command __/stock=*stock_code*__. The stock code must be a valid stock code for [Stooq webpage](https://stooq.com/). It will return the followin message:

> Bot stock: [stock_code] quote is ${value} per share

Where **stock_code** is the requested code and the **value** is the closing value.

# Release note

- v1.0: Functionality working with coupled stock quote bot
- v2.0: Functionality working using a message broker for bots
- v2.1: Fix bugs - Remove files and templates errors
- v2.2: Fix bugs - Filter by room and automatic web socket reconnection
