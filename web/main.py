import tornado.web
import tornado.ioloop
import tornado.gen
import tornado.escape

from asyncudp import AsyncUDPSocket

import sys
import re
import os.path
import datetime
import pathlib

top_dir = pathlib.Path(__file__).parent.parent
sys.path.append(str(top_dir / 'news'))
sys.path.append(str(top_dir / 'db_api'))

from get_best import get_best_posts, get_best_images

def prepare_post(s):

    # handle overflow
    maxlen = 300
    if len(s) > maxlen:
        s = s[:maxlen-3] + '...'

    s = tornado.escape.linkify(s, shorten=True)

    # highlight hashtags
    s = re.sub(r'(#\w+)', r'<span class="hashtag">\1</span>', s)

    # format paragraphs
    s = ''.join('<p>{}</p>'.format(p) for p in s.splitlines())

    return s

def readable_date(timestamp):
    date = datetime.datetime.utcfromtimestamp(timestamp)
    now = datetime.datetime.utcnow()
    if date.year != now.year:
        return format(date, '%d %b %Y at %H:%M')
    if date.date() != now.date():
        return format(date, '%d %b at %H:%M')
    return format(date, '%H:%M')

class PostsHandler(tornado.web.RequestHandler):
    def get(self):
        #posts = []
        #for post in best_posts:
            #text = post.text
            #if len(text) > 200:
                #text = text[:200] + '...'
            #posts.append(text)
        self.render('posts.html', posts=best_posts, readable_date=readable_date, prepare_post=prepare_post)

class ImagesHandler(tornado.web.RequestHandler):
    def get(self):
        '''
        posts = [
            'http://lorempixel.com/800/400', 'http://lorempixel.com/801/400', 'http://lorempixel.com/802/405',
            'http://lorempixel.com/803/400', 'http://lorempixel.com/804/400', 'http://lorempixel.com/805/400',
            'http://lorempixel.com/806/400', 'http://lorempixel.com/807/400', 'http://lorempixel.com/808/400',
        ]
        '''
        posts = media_popular()
        #self.render('images.html', posts=posts)
        self.render('images.html', posts=posts, readable_date=readable_date)

class VideosHandler(tornado.web.RequestHandler):
    def get(self):
        posts = [
            'https://www.youtube.com/embed/UJ1fghCto00', 'https://www.youtube.com/embed/vG9c5egwEYY', 'https://www.youtube.com/embed/rrT6v5sOwJg',
            'https://www.youtube.com/embed/6Dakd7EIgBE', 'https://www.youtube.com/embed/WAe-8xoiDEk'
        ]
        self.render('videos.html', posts=posts)

best_posts = get_best_posts(100)

@tornado.gen.coroutine
def watch_for_new_posts(port):
    s = AsyncUDPSocket(('', port))
    global best_posts
    while True:
        yield s.recvfrom()
        p = get_best_posts(1)
        best_posts = p + best_posts

def main():
    app = tornado.web.Application(
        [
            (r'/', tornado.web.RedirectHandler, {"url": "/posts"}),
            (r'/posts', PostsHandler),
            (r'/images', ImagesHandler),
            (r'/videos', VideosHandler),
        ],
        cookie_secret="SOME_COOKIE_SECRET",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
        )
    app.listen(8888)
    print('server is listening on port 8888')
    loop = tornado.ioloop.IOLoop.current()
    loop.add_callback(watch_for_new_posts, 8953)
    loop.start()


if __name__ == "__main__":
    main()
