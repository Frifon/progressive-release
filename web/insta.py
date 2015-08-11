from instagram import client, subscriptions
from common.models_db import Photo
from common.tools import get_current_timestamp

import sys
sys.path.append(sys.path[0] + '/../news')


access_token="2068329023.d15f6bc.98b280d79e514ddbbe41209a2579a7ac"
client_secret="f377934346184eda8b9b506f5b6f9bd2"


def media_popular():
    if not access_token:
        return 'Missing Access Token'
    try:
        api = client.InstagramAPI(access_token=access_token, client_secret=client_secret)
        media_search = api.media_popular(count=10)
        photos = []

        for media in media_search:
            #photos.append('<img src="%s"/>' % media.get_standard_resolution_url())
            if media.type == 'image':
                photo = Photo(likes_amount=media.like_count, publication_date=media.created_time,
                              description=media.caption, link=media.get_standard_resolution_url(), insta_link=media.link,
                              timestamp=get_current_timestamp())
                #print (media.id, media.link, media.get_low_resolution_url())
                photos.append(photo)

        return photos
    except Exception as e:
        print(e)
    return None
