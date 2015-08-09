# -*- coding: utf8 -*-

__author__ = 'emil.guseynov'

from common.tools import get_current_timestamp
from common.tools import vk_api_authorization
from common.api_requests import Add_request

from collections import deque
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Photo(Base):
    __tablename__ = 'photo'

    """
    :param               id: unique vk id of the photo [int]
    :param         owner_id: unique vk id of the photo owner [int]
    :param        timestamp: timestamp, which shows aggregation time [str]
    :param publication_date: timestamp, which shows publication time [str]
    :param     likes_amount: amount of users, who liked the photo [int]
    :param             link: link to the photo [str]
    :param      description: description of the picture [str]
    """

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    timestamp = Column(Integer)
    publication_date = Column(Integer)
    likes_amount = Column(Integer)
    link = Column(String(100))
    insta_link = Column(String(100))
    description = Column(String(100))

    post_id = Column(Integer, ForeignKey('post.id', ondelete='cascade'))  # new


class Audio(Base):
    __tablename__ = 'audio'

    """
    :param           id: unique vk id of the audio [int]
    :param     owner_id: unique vk id of the audio owner [int]
    :param       artist: name of the song performer [str]
    :param        title: name of the song [str]
    :param    timestamp: timestamp, which shows aggregation time [str]
    :param     duration: song duration in seconds [int]
    :param         link: link to the song [String(100)]
    :param    lyrics_id: unique vk id of the lyrics [int]
    :param     album_id: unique vk id of the album [int]
    :param     genre_id: unique vk id of the genre [int]
               (check https://vk.com/dev/audio_genres for genres info)
    """

    id = Column(Integer, primary_key=True)
    artist = Column(String(100))
    title = Column(String(100))
    owner_id = Column(Integer)
    timestamp = Column(Integer)
    duration = Column(Integer)
    link = Column(String(100))
    lyrics_id = Column(Integer)
    album_id = Column(Integer)
    genre_id = Column(Integer)

    post_id = Column(Integer, ForeignKey('post.id', ondelete='cascade'))  # new


class Video(Base):
    __tablename__ = 'video'

    """
    :param               id: unique vk id of the video [int]
    :param            title: name of the video [str]
    :param         owner_id: unique vk id of the video owner [int]
    :param        timestamp: timestamp, which shows aggregation time [str]
    :param publication_date: timestamp, which shows publication time [str]
    :param         duration: video duration in seconds [int]
    :param     views_amount: amount of users, who watched the video [int]
    :param     likes_amount: amount of users, who liked the video [int]
    :param             link: link to the video [str]
    :param      description: description of the video [str]
    """

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    title = Column(String(100))
    timestamp = Column(Integer)
    description = Column(String(100))
    duration = Column(Integer)
    link = Column(String(100))
    publication_date = Column(Integer)
    views_amount = Column(Integer)
    likes_amount = Column(Integer)

    post_id = Column(Integer, ForeignKey('post.id', ondelete='cascade'))  # new


class Link(Base):
    __tablename__ = 'link'

    """
    :param         url: url of the link [str]
    :param       title: title of the link [str]
    :param description: description of the link [str]
    :param   image_src: link to the image shown with the description [str]
    :param   timestamp: timestamp, which shows aggregation time [str]
    """

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(100))
    title = Column(String(100))
    timestamp = Column(Integer)
    description = Column(String(100))
    image_src = Column(String(100))

    post_id = Column(Integer, ForeignKey('post.id', ondelete='cascade'))  # new


class Attachments:
    requested_attachments = deque()
    initial_stage_done = False
    amount = 0
    total = 0
    list_of_attachments = []
    timestamp = 0
    callback = 0

    def check_readiness(self):
        self.amount += 1
        if self.amount == self.total:
            self.callback(self.list_of_attachments)

    def after_photoGet(self, extended_info):
        photo = self.requested_attachments.popleft()["photo"]
        id = photo["id"]
        owner_id = photo["owner_id"]
        publication_date = photo["date"]
        description = photo["text"]
        link = "https://vk.com/photo{}_{}".format(str(owner_id), str(id))
        if extended_info != False and \
           'likes' in extended_info and \
           'count' in extended_info['likes']:
            likes_amount = extended_info["likes"]["count"]
        else:
            likes_amount = -1

        parsed_photo = Photo(
            id=id, owner_id=owner_id, timestamp=self.timestamp,
            publication_date=publication_date, description=description,
            link=link, likes_amount=likes_amount)
        self.list_of_attachments.append(parsed_photo)
        self.check_readiness()

    def __init__(self, list_of_attachments, callback):
        self.callback = callback
        self.total = len(list_of_attachments)
        timestamp = get_current_timestamp()

        for attachment in list_of_attachments:
            if attachment["type"] == "photo":
                self.requested_attachments.append(attachment)

                values = {
                    "photos": "{}_{}".format(
                        str(attachment["photo"]["owner_id"]),
                        str(attachment["photo"]["id"])),
                    "extended": 1
                }

                Add_request("photos.getById", values, self.after_photoGet)

            elif attachment["type"] == "posted_photo":
                photo = attachment["posted_photo"]

                id = photo["id"]
                owner_id = photo["owner_id"]
                link = photo["photo_604"]

                parsed_photo = Photo(id=id, owner_id=owner_id, link=link)

                self.list_of_attachments.append(parsed_photo)
                self.check_readiness()

            elif attachment["type"] == "audio":
                audio = attachment["audio"]

                id = audio["id"]
                artist = audio["artist"]
                title = audio["title"]
                owner_id = audio["owner_id"]
                duration = audio["duration"]
                link = audio["url"]
                if "lyrics_id" in audio:
                    lyrics_id = audio["lyrics_id"]
                else:
                    lyrics_id = -1
                if "album_id" in audio:
                    album_id = audio["album_id"]
                else:
                    album_id = -1
                if "genre_id" in audio:
                    genre_id = audio["genre_id"]
                else:
                    genre_id = -1

                parsed_audio = Audio(
                    id=id, owner_id=owner_id, timestamp=timestamp,
                    artist=artist, title=title, duration=duration, link=link,
                    lyrics_id=lyrics_id, album_id=album_id, genre_id=genre_id)

                self.list_of_attachments.append(parsed_audio)
                self.check_readiness()

            elif attachment["type"] == "video":
                video = attachment["video"]

                id = video["id"]
                owner_id = video["owner_id"]
                title = video["title"]
                description = video["description"]
                duration = video["duration"]
                link = "https://vk.com/video{}_{}".format(
                    str(owner_id), str(id))
                publication_date = video["date"]
                views_amount = video["views"]

                likes_amount = -1

                parsed_video = Video(
                    id=id, owner_id=owner_id, timestamp=timestamp,
                    title=title, duration=duration, link=link,
                    description=description, publication_date=publication_date,
                    views_amount=views_amount, likes_amount=likes_amount)

                self.list_of_attachments.append(parsed_video)
                self.check_readiness()

            elif attachment["type"] == "link":
                link = attachment["link"]

                url = link["url"]
                title = link["title"]
                description = link["description"]
                
                image_src = ''
                if 'image_src' in link:
                    image_src = link["image_src"]

                parsed_link = Link(url=url, title=title,
                                   description=description,
                                   image_src=image_src)

                self.list_of_attachments.append(parsed_link)
                self.check_readiness()

            else:
                self.amount -= 1
        self.check_readiness()

    def get(self):
        return self.list_of_attachments

    def __str__(self):
        result = ""
        for attachment in self.list_of_attachments:
            result += "\nType: {}\n".format(str(type(attachment)))
            result += "{}\n".format(str(attachment))
        return result


class Post(Base):
    __tablename__ = "post"

    """
    :param               id: unique vk id of the post [int]
    :param         owner_id: unique vk id of the post owner [int]
    :param         owner_id: unique vk id of the post author [int]
    :param        timestamp: timestamp, which shows aggregation time [str]
    :param publication_date: timestamp, which shows publication time [str]
    :param             text: text in the post [str]
    :param     likes_amount: amount of users, who liked the post [int]
    :param   reposts_amount: amount of users, who reposted the post [int]
    :param        post_type: type of the post [str] (possible values:
                             [post, copy, reply, postpone, suggest])
    :param             link: link to the post [str]
    :param      attachments: everything attached to the post [Attachments]
    """

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    author_id = Column(Integer)
    timestamp = Column(Integer)
    publication_date = Column(Integer)
    text = Column(String(100))
    likes_amount = Column(Integer)
    reposts_amount = Column(Integer)
    post_type = Column(String(100))
    link = Column(String(100))
    # attachments = Attachments()
    attachments = []

    def __str__(self):
        return ("Post id: {}\n".format(str(self.id)) +
                "Post type: {}\n".format(self.post_type) +
                "Post owner id: {}\n".format(str(self.owner_id)) +
                "Post author id: {}\n".format(str(self.author_id)) +
                "Publication date: {}\n".format(self.publication_date) +
                "Text:\n{}\n".format(self.text) +
                "Attachments:\n{}\n".format(str(self.attachments)) +
                "Likes amount: {}\n".format(str(self.likes_amount)) +
                "Reposts amount: {}\n".format(str(self.reposts_amount)) +
                "Link: {}\n".format(self.link))


class Wall:
    def __init__(self, owner_id=0, posts=[], timestamp="", link=""):

        """
        :param  owner_id: unique vk id of the wall owner [int]
        :param     posts: list of posts on the wall [list of Post instances]
        :param timestamp: timestamp, which shows aggregation time [str]
        :param      link: link to the wall [str]
        """

        self.owner_id = owner_id
        self.posts = posts
        self.timestamp = timestamp
        self.link = link

    def __str__(self):
        return ("    Owner id: {}\n".format(str(self.owner_id)) +
                "    Amount of posts: {}\n".format(str(len(self.posts))) +
                "    Wall link: {}\n".format(self.link))


class User:
    def __init__(self, id=0, first_name="", last_name="", timestamp="",
                 friends_amount=0, subscribers_amount=0, link="",
                 verified=0, sex=0, bdate="", country="", city="",
                 wall=Wall()):

        """
        :param                   id: unique vk id of the user [int]
        :param           first_name: first name of the user [str]
        :param            last_name: last name of the user [str]
        :param            timestamp: shows aggregation time [str]
        :param       friends_amount: amount of user's friends [int]
        :param   subscribers_amount: amount of user's subscribers [int]
        :param                 link: link to the user [str]
        :param             verified: indicates verified vk users [int->(0|1)]
        :param                  sex: user's sex [int]
                                     (1 - female, 2 - male, 0 - unknown)
        :param                bdate: timestamp, shows user's birthday [str]
        :param              country: country, where user lives [str]
        :param                 city: city, where user lives [str]
        :param                 wall: user's wall [Wall]
        """

        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.timestamp = timestamp
        self.friends_amount = friends_amount
        self.subscribers_amount = subscribers_amount
        self.verified = verified
        self.link = link
        self.sex = sex
        self.bdate = bdate
        self.country = country
        self.city = city
        self.wall = wall

    def __str__(self):
        return ("User id: {}\n".format(str(self.id)) +
                "User name: {} {}\n".format(self.first_name, self.last_name) +
                "User sex: {} (1 - female, 2 - male)\n".format(str(self.sex)) +
                "Birthday: {}\n".format(self.bdate) +
                "Country: {}\n".format(self.country) +
                "City: {}\n".format(self.city) +
                "Amount of friends: {}\n".format(str(self.friends_amount)) +
                "Amount of subscribers: " +
                "{}\n".format(str(self.subscribers_amount)) +
                "User verified: {}\n".format(str(self.verified)) +
                "User link: {}\n".format(self.link) +
                "User wall:\n\n{}".format(str(self.wall)))


class Group:
    def __init__(self, id=0, name="", timestamp="",
                 subscribers_amount=0, link="", verified=0,
                 type="", description="", wall=Wall()):

        """
        :param                   id: unique vk id of the group [int]
        :param                 name: name of the group [str]
        :param            timestamp: shows aggregation time [str]
        :param   subscribers_amount: amount of group subscribers [int]
        :param                 link: link to the group [str]
        :param             verified: indicates verified vk groups [int->(0|1)]
        :param                 type: group type [str->(group|page|event)]
        :param          description: description of the group [str]
        :param                 wall: group wall [Wall]
        """

        self.id = id
        self.name = name
        self.timestamp = timestamp
        self.subscribers_amount = subscribers_amount
        self.link = link
        self.verified = verified
        self.type = type
        self.description = description
        self.wall = wall

    def __str__(self):
        return ("Group id: {}\n".format(str(self.id)) +
                "Group name: {}\n".format(self.name) +
                "Amount of subscribers: " +
                "{}\n".format(str(self.subscribers_amount)) +
                "Group verified: {}\n".format(str(self.verified)) +
                "Type: {}\n".format(self.type) +
                "Description:\n{}\n".format(self.description) +
                "Group link: {}\n".format(self.link) +
                "Group wall:\n{}".format(str(self.wall)))
