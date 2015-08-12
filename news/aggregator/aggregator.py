# -*- coding: utf8 -*-

__author__ = 'a.khachatryan'

from time import time
import sys
import socket

from parsers.wall import Wall_parser
from database.query import add_post, delete_post


def get_users(filename):
    f = open(sys.path[0] + '/' + 'base/' + filename, 'r', encoding="utf-8")
    lines = f.readlines()
    results = []
    for line in lines:
        args = line.split()
        for arg in args:
            if 'id' in str(arg):
                results.append(str(arg)[str(arg).find('id') + 2:])
                break
    return results


def send_notification():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 8953
    MESSAGE = "Hello, World!"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, 'utf-8'), (UDP_IP, UDP_PORT))
    print ("notified")

class Aggregator:
    best_post_delay = 0
    max_old_post = 0
    log = 0
    used_posts = []
    best_post = None
    last_time = 0

    def after_wallparser(this, wall):
        if wall is False:
            return
        if this.log:
            print('Processing ', wall.owner_id)
        posts = wall.posts
        for post in posts:
            if post.id not in this.used_posts and int(time()) - int(post.publication_date) < this.max_old_post:
                if this.best_post is None or post.likes_amount > this.best_post.likes_amount:
                    this.best_post = post

        if this.best_post is not None and int(time()) - this.last_time > this.best_post_delay:
            add_post(this.best_post)
            if this.log:
                print ("new best post id:", this.best_post.id, end='\n\n')
                send_notification()

            this.used_posts.append(this.best_post.id)
            this.last_time = int(time())
            this.best_post = None

    def __init__(this, users, best_post_delay=10, max_old_post=24 * 60 * 60, log=0):
        this.best_post_delay = best_post_delay
        this.max_old_post = max_old_post
        this.log = log

        this.last_time = int(time())

        print('Aggregator started')

        while (1):
            for user in users:
                Wall_parser(user, this.after_wallparser)
