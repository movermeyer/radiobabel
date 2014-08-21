# future imports
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# stdlib imports
import os
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
        track = self.client.track('6MeNtkNT4ENE5yohNvGqd4')
        self.assertDictEqual(track, {
            "album": {
                'name': 'Arnold / Sun Splash',
                'source_type': 'spotify',
                'source_id': '7afslC4eAFOeXVV2a4ZiIw',
            },
            'artists': [
                {
                    'name': 'Luke Million',
                    'source_type': 'spotify',
                    'source_id': '1khu4DLsGK5MWLbUlfKkgz',
                },
            ],
            'track_number': 1,
            'source_id': '6MeNtkNT4ENE5yohNvGqd4',
            'name': 'Arnold',
            'duration_ms': 249020,
            'preview_url': 'https://p.scdn.co/mp3-preview/8e9273de2ee2c3df040fe2f2a4c9117007431396',
            'source_type': 'spotify',
            'image_small': 'https://i.scdn.co/image/c1286d79f143a3d6c197cf215d1db79cd6ddabe0',
            'image_medium': 'https://i.scdn.co/image/b883173d6682bf33f5b8d909467b07639af522c8',
            'image_large': 'https://i.scdn.co/image/804bb6e41d095ff193c5136a3a98a1482acbb983',
        })

    def test_lookup_with_bad_id(self):
        """Spotify: Looking up an invalid track raises the appropriate error
        """
        with self.assertRaises(TrackNotFound):
            self.client.track('1')


class SearchTests(unittest.TestCase):

    def setUp(self):
        load_config()
        self.client = SpotifyClient()

    def test_search_returns_results(self):
        """Spotify: Test that search results are returned in the correct format
        """
        results = self.client.search('wugazi')
        self.assertGreater(len(results), 0)
