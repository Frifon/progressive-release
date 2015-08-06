# -*- coding: utf8 -*-

__author__ = 'dimagalov'

from common.tools import vk_api_authorization
from common.models_db import User
from common.tools import get_current_timestamp
from parsers.wall import parse_wall


def get_user_id(user):
    try:
        return user["id"]
    except:
        print("Problem occured while getting user id")


def get_user_first_name(user):
    try:
        return user["first_name"]
    except:
        print("Problem occured while getting user first name")


def get_user_last_name(user):
    try:
        return user["last_name"]
    except:
        print("Problem occured while getting user last name")


def get_friends_amount(vk_api, user):
    try:
        id = get_user_id(user)

        values = {
            "user_id": id
        }

        friends = vk_api.method("friends.get", values)

        return friends["count"]
    except:
        print("Problem occured while getting user friends amount")


def get_subscribers_amount(user):
    try:
        return user["followers_count"]
    except:
        print("Problem occured while getting subscribers amount")


def get_user_verified(user):
    try:
        return user["verified"]
    except:
        print("Problem occured while getting user verification")


def get_user_sex(user):
    try:
        return user["sex"]
    except:
        print("Problem occured while getting user sex")


def get_user_bdate(user):
    try:
        return user["bdate"]
    except:
        print("Problem occured while getting user bdate")


def get_user_country(user):
    try:
        return user["country"]["title"]
    except:
        print("Problem occured while getting user country")


def get_user_city(user):
    try:
        return user["city"]["title"]
    except:
        print("Problem occured while getting user city")


def get_user_link(user):
    try:
        return "https://vk.com/id" + str(get_user_id(user))
    except:
        print("Problem occured while getting user link")


def get_user_wall(user):
    try:
        return parse_wall(get_user_id(user))
    except:
        print("Problem occured while getting user wall")


def parse_user(vk_api, user):
    id = get_user_id(user)
    first_name = get_user_first_name(user)
    last_name = get_user_last_name(user)
    timestamp = get_current_timestamp()
    friends_amount = get_friends_amount(vk_api, user)
    subscribers_amount = get_subscribers_amount(user)
    verified = get_user_verified(user)
    link = get_user_link(user)
    sex = get_user_sex(user)
    bdate = get_user_bdate(user)
    country = get_user_country(user)
    city = get_user_city(user)
    wall = get_user_wall(user)

    parsed_user = User(id=id, first_name=first_name, last_name=last_name,
                       timestamp=timestamp, link=link, verified=verified,
                       friends_amount=friends_amount, sex=sex,
                       subscribers_amount=subscribers_amount,
                       bdate=bdate, country=country, city=city, wall=wall)

    return parsed_user


def parse_user_pages(user_ids):
    vk_api = vk_api_authorization()

    values = {
        "user_ids": user_ids,
        "fields": "followers_count,verified,sex,bdate,country,city"
    }

    users = vk_api.method("users.get", values)

    parsed_users = [parse_user(vk_api, user) for user in users]

    return parsed_users
