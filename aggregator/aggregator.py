# -*- coding: utf8 -*-

__author__ = 'a.khachatryan'

from parsers.wall import parse_wall
from database.query import add_post, delete_post
from time import time

def get_users(filename):
    f = open('base/' + filename, 'r', encoding="utf-8")
    lines = f.readlines()
    results = []
    for line in lines:
        args = line.split()
        for arg in args:
            if 'id' in str(arg):
                results.append(str(arg)[str(arg).find('id') + 2:])
                break
    return results

def aggregator(users, best_post_delay = 10, max_old_post = 24 * 60 * 60, log = 0):
    last_time = int(time())
    best_post = None
    used_posts = []

    while (1):
        for user in users:
            if log:
                print("User", user, "scanning")
            posts = parse_wall(user).posts
            for post in posts:
                if post.id not in used_posts and int(time()) - int(post.publication_date) < max_old_post:
                   if best_post is None or post.likes_amount > best_post.likes_amount:
                        best_post = post
                        if log:
                            print ("new best post updated:", best_post.id)
            if best_post != None and int(time()) - last_time > best_post_delay:
                add_post(best_post)
                if log:
                    print ("new best post id:", best_post.id)
                    print ('')
                used_posts.append(best_post.id)
                last_time = int(time())
                best_post = None

