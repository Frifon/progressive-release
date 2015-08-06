# -*- coding: utf8 -*-

__author__ = 'vient'

from common.tools import get_current_timestamp
from common.models_db import Wall
from common.api_requests import Add_request
from parsers.post import parse_post


def get_wall_link(id):
    return "https://vk.com/wall{}?own=1".format(id)


class Wall_parser:
    user = 0
    callback = 0

    def after_wallget(this, wall):
        parsed_posts = [parse_post(post) for post in wall["items"]]
        parsed_wall = Wall(owner_id=this.user,
                           posts=parsed_posts,
                           timestamp=get_current_timestamp(),
                           link=get_wall_link(this.user))

        this.callback(parsed_wall)

    def __init__(this, user, callback):
        this.user = user
        this.callback = callback

        values = {
            "owner_id": user,
            "filter": "owner"
        }

        Add_request("wall.get", values, this.after_wallget)


# !!!
# CODE UNDER THIS LINE IS OBSOLETE AND WILL BE DELETED IN FUTURE RELEASES
# !!!

# def parse_wall(id):
#
#     ''' WARNING! parse_wall takes only id, not a screen name '''
#
#     vk_api = vk_api_authorization()
#
#     if vk_api == None:
#         print('Something went wrong. Maybe wrong credentials?')
#         exit(0)
#
#     values = {
#         "owner_id": id,
#         "filter": "owner"
#     }
#
#     while (1):
#         try:
#             wall = vk_api.method("wall.get", values)
#             break
#         except ApiError:
#             print ('Too many requests per second. Trying again.')
#
#     parsed_posts = [parse_post(post) for post in wall["items"]]
#
#     parsed_wall = Wall(owner_id=id, posts=parsed_posts,
#                        timestamp=get_current_timestamp(),
#                        link=get_wall_link(id))
#
#     return parsed_wall
