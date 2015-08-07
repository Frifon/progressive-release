import socket
import collections

from tornado.concurrent import Future
from tornado.ioloop import IOLoop

__all__ = ['AsyncUDPSocket']

class AsyncUDPSocket:
    def __init__(self, addr=None):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if addr is not None:
            self.bind(addr)
        self._readers = collections.deque()
        self._writers = collections.deque()
        self._mode = IOLoop.ERROR
        IOLoop.current().add_handler(self._s, self._handle_events, self._mode)

    def bind(self, addr):
        self._s.bind(addr)

    def recvfrom(self):
        f = Future()
        if not self._readers:
            assert not self._mode & IOLoop.READ
            self._mode |= IOLoop.READ
            self._update_handler()
        self._readers.append(f)
        return f

    def sendto(self, *args):
        f = Future()
        if not self._writers:
            assert not self._mode & IOLoop.WRITE
            self._mode |= IOLoop.WRITE
            self._update_handler()
        self._writers.append((f, args))
        return f

    def _do_read(self, f):
        res = self._s.recvfrom(2**17)
        f.set_result(res)

    def _do_write(self, f, args):
        res = self._s.sendto(*args)
        f.set_result(res)

    def _handle_events(self, ss, events):
        if events & IOLoop.READ:
            self._do_read(self._readers.popleft())
            if not self._readers:
                self._mode ^= IOLoop.READ
                self._update_handler()
        if events & IOLoop.WRITE:
            self._do_write(*self._writers.popleft())
            if not self._writers:
                self._mode ^= IOLoop.WRITE
                self._update_handler()
        if events & IOLoop.ERROR:
            self.close()

    def _update_handler(self):
        IOLoop.current().update_handler(self._s, self._mode)

    def close(self):
        IOLoop.current().remove_handler(self._s)
        self._s.close()

