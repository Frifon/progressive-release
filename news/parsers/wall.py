# -*- coding: utf8 -*-

__author__ = 'vient'

from common.tools import get_current_timestamp
from common.models_db import Wall
from common.api_requests import Add_request
from parsers.post import Post_parser


def get_wall_link(id):
    return "https://vk.com/wall{}?own=1".format(id)


class Wall_parser:
    user = 0
    callback = 0
    parsed_posts = []
    posts_amount = 0
    posts_total = 0

    def after_postparser(self, parsed_post):
        self.parsed_posts.append(parsed_post)
        self.posts_amount += 1
        if self.posts_amount == self.posts_total:
            parsed_wall = Wall(owner_id=self.user,
                               posts=self.parsed_posts,
                               timestamp=get_current_timestamp(),
                               link=get_wall_link(self.user))

            self.callback(parsed_wall)

    def after_wallget(self, wall):
        # print(wall)
        if not wall:
            self.callback(False)
            return
        self.posts_total = len(wall['items'])

        for post in wall['items']:
            Post_parser(post, self.after_postparser)

    def __init__(self, user, callback):
        self.user = user
        self.callback = callback

        values = {
            "owner_id": user,
            "filter": "owner"
        }

        Add_request("wall.get", values, self.after_wallget)
