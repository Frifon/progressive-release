# -*- coding: utf8 -*-

__author__ = 'dimagalov'

from common.tools import vk_api_authorization
from common.models_db import Group
from common.tools import get_current_timestamp
from parsers.wall import parse_wall


def get_group_id(group):
    try:
        return -1 * group["id"]
    except:
        print("Problem occured while getting group id")


def get_group_name(group):
    try:
        return group["name"]
    except:
        print("Problem occured while getting group name")


def get_subscribers_amount(group):
    try:
        return group["members_count"]
    except:
        print("Problem occured while getting subscribers amount")


def get_group_verified(group):
    try:
        return group["verified"]
    except:
        print("Problem occured while getting group verification")


def get_group_type(group):
    try:
        return group["type"]
    except:
        print("Problem occured while getting group type")


def get_group_description(group):
    try:
        return group["description"]
    except:
        print("Problem occured while getting group description")


def get_group_link(group):
    try:
        return "https://vk.com/club" + str(get_group_id(group))
    except:
        print("Problem occured while getting group link")


def get_group_wall(group):
    try:
        return parse_wall(get_group_id(group))
    except:
        print("Problem occured while getting group wall")


def parse_group(group):
    id = get_group_id(group)
    name = get_group_name(group)
    timestamp = get_current_timestamp()
    subscribers_amount = get_subscribers_amount(group)
    verified = get_group_verified(group)
    type = get_group_type(group)
    description = get_group_description(group)
    link = get_group_link(group)
    wall = get_group_wall(group)

    parsed_group = Group(id=id, name=name, timestamp=timestamp, link=link,
                         subscribers_amount=subscribers_amount, wall=wall,
                         verified=verified, type=type, description=description)

    return parsed_group


def parse_group_pages(group_ids):
    vk_api = vk_api_authorization()

    values = {
        "group_ids": group_ids,
        "fields": "members_count,verified,description"
    }

    groups = vk_api.method("groups.getById", values)

    parsed_groups = [parse_group(group) for group in groups]

    return parsed_groups
