# -*- coding: utf8 -*-

__author__ = 'vient'

from common.tools import vk_api_authorization
from vk_api.vk_api import ApiError

from collections import deque


class Add_request:
    execute_limit = 25
    requests = deque()
    callbacks = deque()
    _execute_mutex = False  # Preventing stack overflow

    def execute_requests(this):
        this._execute_mutex = True

        vk_api = vk_api_authorization()
        if vk_api is None:
            print('Something went wrong. Maybe wrong credentials?')
            exit(0)

        while len(this.requests) > 0:
            current_requests = 0
            request = 'return ['

            while len(this.requests) > 0 and current_requests < this.execute_limit:
                now = this.requests.popleft()
                request += 'API.{req[0]}({req[1]}), '.format(req=now)
                current_requests += 1
            request = (request[:-2] + '];').replace("'", '"')

            while True:
                try:
                    resp = vk_api.method("execute", {"code": request})
                    break
                except ApiError:
                    print('Too many requests per second. Trying again.')

            index = 0
            while current_requests > 0:
                now = this.callbacks.popleft()(resp[index])
                index += 1
                current_requests -= 1

        this._execute_mutex = False

    def __init__(this, method, values, callback):
        this.requests.append([method, str(values)])
        this.callbacks.append(callback)
        if this._execute_mutex is False and len(this.requests) >= this.execute_limit:
            this.execute_requests()
