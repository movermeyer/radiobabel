# future imports
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# stdlib imports
import logging

# third-party imports
import requests

# local imports
from radiobabel.errors import TrackNotFound, PlaylistNotFound
from .utils import random_pick


logger = logging.getLogger('radiobabel.backends.lastfm')


def _transform_track(track):
    """Transform result into a format that
    more closely matches our unified API.
    """
    large_artwork = None
    medium_artwork = None
    small_artwork = None

    if track['artwork_url']:
        large_artwork = (track['artwork_url']).replace('large', 't500x500')
        medium_artwork = (track['artwork_url']).replace('large', 't300x300')
        small_artwork = (track['artwork_url']).replace('large', 't67x67')

    transformed_track = dict([
        ('source_type', 'lastfm'),
        ('source_id', track['id']),
        ('name', track['title']),
        ('duration_ms', track['duration']),
        ('preview_url', track.get('stream_url')),
        ('uri', 'lastfm:song/' + track['title'] + '.' + str(track['id'])),
        ('track_number', 0),
        ('image_small', small_artwork),
        ('image_medium', medium_artwork),
        ('image_large', large_artwork),
    ])
    transformed_track['artists'] = [
        dict([
            ('source_type', 'lastfm'),
            ('source_id', track['user']['id']),
            ('name', track['user']['username']),
        ]),
    ]
    transformed_track['album'] = None

    return transformed_track


def _transform_playlist(playlist):
    """Transform result into a format that more
    closely matches our unified API.
    """
    transformed_playlist = dict([
        ('source_type', 'lastfm'),
        ('source_id', playlist.id),
        ('name', playlist.title),
        ('tracks', playlist.track_count),
    ])
    return transformed_playlist


class LastFMClient(object):

    def __init__(self, client_id):
        """Initialise lastfm API client.
        """
        pass

    def login_url(self, callback_url, client_id, client_secret):
        """Generates a login url, for the user to authenticate the app."""
        pass

    def exchange_code(self, code, callback_url, client_id, client_secret):
        """Fetch auth and user data from the lastfm api

        Returns a dictionary of a auth and user object.
        """
        pass

    def lookup_track(self, track_id):
        """Lookup a single track using the lastfm API
        """
        logger.info('Track lookup: {0}'.format(track_id))

        pass

    def search_tracks(self, query, limit=200, offset=0):
        """Search for tracks using the lastfm API
        """
        logger.info('Searching: Limit {0}, Offset {1}'.format(limit, offset))

        pass

    def fetch_associated_track(self, artist):
        """Fetch a random associated track, using the lastfm API.
        """
        pass

    def playlists(self, user_id, token):
        """Lookup user playlists using the lastfm Web API

        Returns standard radiobabel playlist list response.
        """
        logger.info('Playlist lookup: {0}'.format(user_id))

        pass

    def playlist_tracks(self, playlist_id, user_id, token, limit=20, offset=0):
        """Search for tracks using the lastfm API
        """
        logger.info('Searching: Limit {0}, Offset {1}'.format(limit, offset))

        pass
