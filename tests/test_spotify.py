# future imports
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# stdlib imports
import unittest

# local imports
from radiobabel import SpotifyClient
from radiobabel.errors import TrackNotFound
from radiobabel.test_utils import load_config


class LookupTests(unittest.TestCase):

    def setUp(self):
        load_config()
        self.client = SpotifyClient()

    def test_lookup(self):
        """Spotify: Looking up a valid track (str) returns the expected data
        """
        track = self.client.lookup_track('6MeNtkNT4ENE5yohNvGqd4')
        self.assertDictEqual(track, {
            'source_type': 'spotify',
            'source_id': '6MeNtkNT4ENE5yohNvGqd4',
            'name': 'Arnold',
            'artists': [
                {
                    'source_type': 'spotify',
                    'source_id': '1khu4DLsGK5MWLbUlfKkgz',
                    'name': 'Luke Million',
                }
            ],
            'album': {
                'source_type': 'spotify',
                'source_id': '7afslC4eAFOeXVV2a4ZiIw',
                'name': 'Arnold / Sun Splash',
            },
            'duration_ms': 249020,
            'preview_url': 'https://p.scdn.co/mp3-preview/8e9273de2ee2c3df040fe2f2a4c9117007431396',
            'uri': 'spotify:track:6MeNtkNT4ENE5yohNvGqd4',
            'track_number': 1,
            'image_small': 'https://i.scdn.co/image/804bb6e41d095ff193c5136a3a98a1482acbb983',
            'image_medium': 'https://i.scdn.co/image/b883173d6682bf33f5b8d909467b07639af522c8',
            'image_large': 'https://i.scdn.co/image/c1286d79f143a3d6c197cf215d1db79cd6ddabe0',
        })

    def test_lookup_with_bad_id(self):
        """Spotify: Looking up an invalid track raises the appropriate error
        """
        with self.assertRaises(TrackNotFound):
            self.client.lookup_track('1')


class SearchTests(unittest.TestCase):

    def setUp(self):
        load_config()
        self.client = SpotifyClient()

    def test_search_returns_results(self):
        """Spotify: Test that search results are returned in the correct format
        """
        results = self.client.search_tracks('everything is awesome')
        self.assertGreater(len(results), 0)
