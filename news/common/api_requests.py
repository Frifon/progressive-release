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

    # add_photo_request() variables
    photo_limit = 100    # how much photos to get in 1 request
    photo_values_in_process = deque()
    photo_values = deque()
    photo_callbacks = deque()


    def photos_callback(responce):
        self = Add_request 
        popped = 0
        if self._debug:
            print('photos_callback')

        if responce is False:
            for i in range(self.photo_limit):
                self.photo_values_in_process.popleft()
                self.photo_callbacks.popleft()(False)
            return

        for photo_info in responce:
            processed = False

            while len(self.photo_values_in_process) > 0 and not processed:
                photo_id = self.photo_values_in_process.popleft().split('_')[1]
                if photo_id != str(photo_info['id']):
                    if self._debug:
                        print('BAD', photo_id, '!=', photo_info['id'], end=' ')
                    self.photo_callbacks.popleft()(False)
                else:
                    if self._debug:
                        print("GOOD", end=' ')
                    self.photo_callbacks.popleft()(photo_info)
                    processed = True
                if self._debug:
                    print(len(self.photo_values), len(self.photo_values_in_process), len(self.photo_callbacks))
                popped += 1

                if self._debug and len(self.photo_values_in_process) > 0:
                    print(self.photo_values_in_process[0], end=' ')

            if len(self.photo_values_in_process) == 0 and not processed:
                print('FATAL ERROR IN news.common.api_requests.Add_request.photos_callback')
                print('REQUEST FOR PHOTO IS MISSING')
                exit(-1)

        while popped < self.photo_limit:
            self.photo_values_in_process.popleft()
            self.photo_callbacks.popleft()(False)
            popped += 1

    def execute_requests(self):
        Add_request._execute_mutex = True

        while True:
            try:
                if self._debug:
                    print('try', end=' ')       # DEBUG PRINT
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
        if self._debug:
            print('\nsuccess!')                 # DEBUG PRINT

        while len(self.requests) >= self.execute_limit:
            if self._debug:
                print('execute started...', end=' ') # DEBUG PRINT
                pass

            current_requests = 0
            request = 'return ['

            while len(self.requests) > 0 and current_requests < self.execute_limit:
                now = self.requests.popleft()
                if self._debug:
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
                    if self._debug:
                        traceback.print_exc()
                    pass

            if self._debug:
                print('connected')            # DEBUG PRINT
                pass

            index = 0
            while current_requests > 0:
                if self._debug:
                    print('.', end=' ')       # DEBUG PRINT
                self.callbacks.popleft()(resp[index])
                index += 1
                current_requests -= 1

            if self._debug:
                print('\n---------------')    # DEBUG PRINT

        Add_request._execute_mutex = False

    def add_photo_request(self, values, callback):
        self.photo_values.append(values['photos'])
        self.photo_callbacks.append(callback)
        if self._debug:
            print('add_photo_request', values['photos'], len(self.photo_values), len(self.photo_values_in_process), len(self.photo_callbacks))
        if len(self.photo_values) >= self.photo_limit:
            final_request = []
            for i in range(self.photo_limit):
                req = self.photo_values.popleft()
                final_request.append(req + ',')
                self.photo_values_in_process.append(req)

            final_request = ''.join(final_request)
            final_values = {
                'photos': final_request,
                'extended': 1
            }
            self.requests.append(['photos.getById', str(final_values)])
            self.callbacks.append(self.photos_callback)

            if self._execute_mutex is False and \
               len(self.requests) >= self.execute_limit:
                self.execute_requests(self)

    def __init__(self, method, values, callback):
        self = Add_request

        if (method == 'photos.getById'):
            self.add_photo_request(self, values, callback)
            return

        self.requests.append([method, str(values)])
        self.callbacks.append(callback)
        if self._execute_mutex is False and \
           len(self.requests) >= self.execute_limit:
            self.execute_requests(self)
