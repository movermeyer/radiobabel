# future imports
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# stdlib imports
import logging
import re
import string
import unicodedata
import urllib

# third-party imports
#from gdata import youtube
import requests

# local imports
from radiobabel.errors import TrackNotFound, PlaylistNotFound
from .utils import random_pick


logger = logging.getLogger('radiobabel.backends.youtube')


def safe_url(uri):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    safe_uri = unicodedata.normalize(
        'NFKD',
        unicode(uri)
    ).encode('ASCII', 'ignore')

    return re.sub(
        '\s+',
        ' ',
        ''.join(c for c in safe_uri if c in valid_chars)
    ).strip()


def _make_request(url, params=None):
    """Make a HTTP request to the Youtube API using the requests library
    """
    response = requests.get(url, params=params)
    # raise an exception if 400 <= response.status_code <= 599
    response.raise_for_status()
    return response.json()


def _make_post_request(url, data):
    """Make a HTTP request to the Youtube API using the requests library
    """
    response = requests.post(url, data=data)
    # raise an exception if 400 <= response.status_code <= 599
    response.raise_for_status()
    return response.json()


def _make_oauth_request(url, token, params=None):
    # Use token in authorization header of call
    headers = {'Authorization': 'Bearer {}'.format(token)}
    response = requests.get(url, headers=headers, params=params)
    # raise an exception if 400 <= response.status_code <= 599
    response.raise_for_status()
    return response.json()


def _transform_search_response(search_results, offset):
    """Transform a result returned from the Youtube API into a format we
    can return to clients/use to populate the database.
    """
    total_results = int(search_results['pageInfo']['totalResults'])
    if total_results > 1000:
        total_results = 1000

    _track_list = [None for x in range(total_results)]
    for idx, track in enumerate(search_results['items']):
        transformed_track = _transform_track(track)
        _track_list[offset + idx] = transformed_track
    return _track_list


def _transform_track(track):
    """Transform result into a format that more
    closely matches our unified API.
    """
    if isinstance(track['id'], dict):
        track_id = track['id']['videoId']
    else:
        track_id = track['id']

    uri = 'youtube:video/%s.%s' % (
        safe_url(track['snippet']['title']), track_id
    )
    transformed_track = dict([
        ('source_type', 'youtube'),
        ('source_id', track_id),
        ('name', track['snippet']['title']),
        ('duration_ms', 0),
        ('preview_url', None),
        ('uri', uri),
        ('track_number', 0),
        ('artists', None),
        ('album', None),
        ('image_small', None),
        ('image_medium', None),
        ('image_large', None),
    ])
    if 'thumbnails' in track['snippet']:
        images = track['snippet']['thumbnails']
        transformed_track['image_small'] = images['default']['url']
        transformed_track['image_medium'] = images['medium']['url']
        transformed_track['image_large'] = images['high']['url']

    return transformed_track


class YoutubeClient(object):

    def __init__(self):
        """Initialise Youtube API client.
        """
        self.yt_api_endpoint = 'https://www.googleapis.com/youtube/v3/'
        self.yt_key = 'AIzaSyAl1Xq9DwdE_KD4AtPaE4EJl3WZe2zCqg4'

    def login_url(self, callback_url, client_id, client_secret):
        """Generates a login url, for the user to authenticate the app."""
        params = {
            'client_id': client_id,
            'redirect_uri': callback_url,
            'scope': 'https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/userinfo.profile',
            'response_type': 'code',
            'access_type': 'offline',
        }
        params = urllib.urlencode(params)
        url = 'https://accounts.google.com/o/oauth2/auth?{0}'.format(params)
        return url

    def exchange_code(self, code, callback_url, client_id, client_secret):
        """Fetch auth and user data from the spotify api

        Returns a dictionary of a auth and user object.
        """
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': callback_url,
            'client_id': client_id,
            'client_secret': client_secret
        }

        auth_data = _make_post_request(
            'https://accounts.google.com/o/oauth2/token',
            data
        )

        params = {'alt': 'json', 'access_token': auth_data['access_token']}
        r = requests.get(
            'https://www.googleapis.com/oauth2/v1/userinfo',
            params=params
        )
        user_obj = r.json()

        user_data = {
            'id': user_obj['id'],
            'country': user_obj['locale'],
            'username': user_obj['name'],
            'profile_url': user_obj['link'],
            'avatar_url': user_obj['picture']
        }

        response = {
            'auth': auth_data,
            'user': user_data
        }

        return response

    def lookup_track(self, track_id):
        """Lookup a single track using the Youtube API
        """
        logger.info('Track lookup: {0}'.format(track_id))

        params = {
            'id': track_id,
            'part': 'snippet',
            'key': self.yt_key,
        }

        try:
            track = _make_request(self.yt_api_endpoint+'videos', params)
        except:
            raise TrackNotFound('Youtube: {0}'.format(track_id))

        return _transform_track(track['items'][0])

    def search_tracks(self, query, limit=20, offset=0):
        """Search for tracks using the Youtube API
        """
        if limit > 50:
            limit = 50

        logger.info('Searching: Limit {0}, Offset {1}'.format(limit, offset))
        params = {
            'part': 'snippet',
            'maxResults': limit,
            'type': 'video',
            'q': query,
            'key': self.yt_key,
        }

        response = _make_request(self.yt_api_endpoint+'search', params)
        tracks = _transform_search_response(response, offset)
        return tracks

    def fetch_associated_track(self, source_id):
        logger.info('Associated videos: {0}'.format(source_id))
        params = {
            'part': 'snippet',
            'maxResults': 10,
            'type': 'video',
            'relatedToVideoId': source_id,
            'key': self.yt_key,
        }

        response = _make_request(self.yt_api_endpoint+'search', params)
        track = random_pick(response['items'])

        return _transform_track(track)
