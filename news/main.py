# -*- coding: utf8 -*-

__author__ = 'dimagalov'

from aggregator.aggregator import get_users, Aggregator
from database.query import delete_all

print('Hope you\'ve created database (database\\create_db.py)')

delete_all()

Aggregator(get_users('users_10000'), best_post_delay=10,
           max_old_post=24 * 60 * 60, log=1)
