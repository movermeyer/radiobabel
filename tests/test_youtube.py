# future imports
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# stdlib imports
import unittest

# local imports
from radiobabel import YoutubeClient
from radiobabel.errors import TrackNotFound
from radiobabel.test_utils import load_config


class LookupTests(unittest.TestCase):

    def setUp(self):
        load_config()
        self.client = YoutubeClient()

    def test_lookup(self):
        """Youtube: Looking up a valid track (str) returns the expected data
        """
        track = self.client.lookup_track('-catC4tBVyY')
        self.assertDictEqual(track, {
            'source_type': 'youtube',
            'source_id': '-catC4tBVyY',
            'name': 'Frank | Official Trailer',
            'artists': [],
            'album': None,
            'duration_ms': 119000,
            'preview_url': 'youtube:video/Frank Official Trailer.-catC4tBVyY',
            'uri': 'youtube:video/Frank Official Trailer.-catC4tBVyY',
            'track_number': 0,
            'image_small': 'https://i.ytimg.com/vi/-catC4tBVyY/default.jpg',
            'image_medium': 'https://i.ytimg.com/vi/-catC4tBVyY/mqdefault.jpg',
            'image_large': 'https://i.ytimg.com/vi/-catC4tBVyY/hqdefault.jpg',
        })

    def test_lookup_with_bad_id(self):
        """Youtube: Looking up an invalid track raises the appropriate error
        """
        with self.assertRaises(TrackNotFound):
            self.client.lookup_track('1')


class SearchTests(unittest.TestCase):

    def setUp(self):
        load_config()
        self.client = YoutubeClient()

    def test_search_returns_results(self):
        """Youtube: Test that search results are returned in the correct format
        """
        results = self.client.search_tracks('everything is awesome')
        self.assertGreater(len(results), 0)
