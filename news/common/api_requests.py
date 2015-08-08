# -*- coding: utf8 -*-

__author__ = 'vient'

from common.tools import vk_api_authorization
from vk_api.vk_api import ApiError

from collections import deque
import traceback


class Add_request:
    _debug = False

    execute_limit = 25
    requests = deque()
    callbacks = deque()
    _execute_mutex = False  # Preventing stack overflow

    def execute_requests(this):
        Add_request._execute_mutex = True

        while True:
            try:
                # print('try', end=' ')       # DEBUG PRINT
                vk_api = vk_api_authorization()
                break
                '''
                if vk_api is None:
                    print('Something went wrong. Maybe wrong credentials?')
                    exit(0)
                '''
            except KeyboardInterrupt:
                traceback.print_exc()
                exit(0)
            except:
                pass
        # print('\nsuccess!')                 # DEBUG PRINT

        while len(this.requests) > 0:
            if this._debug:
                # print('execute started...', end=' ') # DEBUG PRINT
                pass

            current_requests = 0
            request = 'return ['

            while len(this.requests) > 0 and current_requests < this.execute_limit:
                now = this.requests.popleft()
                if this._debug:
                    print('Added request ', now[0], ', values ', now[1])    # DEBUG PRINT
                request += 'API.{req[0]}({req[1]}), '.format(req=now)
                current_requests += 1
            request = (request[:-2] + '];').replace("'", '"')

            while True:
                try:
                    resp = vk_api.method("execute", {"code": request})
                    break
                except KeyboardInterrupt:
                    traceback.print_exc()
                    exit(0)
                except ApiError:
                    print('Too many requests per second. Trying again.')
                except:
                    # traceback.print_exc()
                    pass

            if this._debug:
                # print('connected')          # DEBUG PRINT
                pass

            index = 0
            while current_requests > 0:
                if this._debug:
                    print('.', end=' ')       # DEBUG PRINT
                now = this.callbacks.popleft()(resp[index])
                index += 1
                current_requests -= 1

            if this._debug:
                print('\n---------------')    # DEBUG PRINT

        Add_request._execute_mutex = False

    def __init__(this, method, values, callback):
        Add_request.requests.append([method, str(values)])
        Add_request.callbacks.append(callback)
        if Add_request._execute_mutex is False and \
           len(Add_request.requests) >= Add_request.execute_limit:
            Add_request.execute_requests(Add_request)
