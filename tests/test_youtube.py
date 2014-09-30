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
        self.maxDiff = None
        track = self.client.lookup_track('-catC4tBVyY')
        self.assertDictEqual(track, {
            'album': None,
            'image_large': 'https://i.ytimg.com/vi/-catC4tBVyY/hqdefault.jpg',
            'image_medium': 'https://i.ytimg.com/vi/-catC4tBVyY/mqdefault.jpg',
            'duration_ms': 119000,
            'name': 'Frank | Official Trailer',
            'image_small': 'https://i.ytimg.com/vi/-catC4tBVyY/default.jpg',
            'uri': 'youtube:video/Frank Official Trailer.-catC4tBVyY',
            'preview_url': 'youtube:video/Frank Official Trailer.-catC4tBVyY',
            'source_type': 'youtube',
            'artists': [],
            'source_id': '-catC4tBVyY',
            'track_number': 0
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


class FetchAssociatedTrackTests(unittest.TestCase):

    def setUp(self):
        load_config()
        self.client = YoutubeClient()

    def test_fetch_returns_result(self):
        """Youtube: Test that a fetch, returns a random track.
        """
        track_id = '-catC4tBVyY'
        track = self.client.fetch_associated_track(track_id)

        self.assertNotEqual(track['source_id'], track_id)
