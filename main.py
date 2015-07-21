# -*- coding: utf8 -*-

__author__ = 'dimagalov'

from aggregator.aggregator import get_users, aggregator
from database.query import delete_all

delete_all()

aggregator(get_users('users_club_22079806'), best_post_delay = 10, max_old_post = 24 * 60 * 60, log = 1)