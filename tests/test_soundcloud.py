# future imports
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# stdlib imports
import os
import unittest

# local imports
from radiobabel import SoundcloudClient
from radiobabel.errors import TrackNotFound
from radiobabel.test_utils import load_config


class ClientInitializationTests(unittest.TestCase):

    def test_no_client_id(self):
        """Test that proper error is raised when no client id is provided
        """
        with self.assertRaises(TypeError):
            SoundcloudClient()

    def test_client_id_passed_in(self):
        """Soundcloud: Client ID is correctly read from passed-in args
        """
        try:
            SoundcloudClient('XXXX')
        except:
            self.fail("Exception unexpectedly raised")


class LookupTests(unittest.TestCase):

    def setUp(self):
        load_config()
        self.client = SoundcloudClient(os.environ['SOUNDCLOUD_CLIENT_ID'])

    def test_valid_lookup_str(self):
        """Soundcloud: Looking up a valid track (str) returns the expected data
        """
        track = self.client.lookup_track('18048610')
        self.assertDictEqual(track, {
            "source_type": "soundcloud",
            "source_id": 18048610,
            "name": "Sleep Rules Everything Around Me",
            "artists": [
                {
                    "source_type": "soundcloud",
                    "source_id": 5613872,
                    "name": "WUGAZI",
                }
            ],
            "album": None,
            "duration_ms": 199180,
            "preview_url": "https://api.soundcloud.com/tracks/18048610/stream",
            "uri": "soundcloud:song.18048610",
            "track_number": 0,
            "image_small": "https://i1.sndcdn.com/artworks-000008722839-oyzy1n-t67x67.jpg?debc7fd",
            "image_medium": "https://i1.sndcdn.com/artworks-000008722839-oyzy1n-t300x300.jpg?debc7fd",
            "image_large": "https://i1.sndcdn.com/artworks-000008722839-oyzy1n-t500x500.jpg?debc7fd",
        })

    def test_valid_lookup_int(self):
        """Soundcloud: Looking up a valid track (str) returns the expected data
        """
        track = self.client.lookup_track(18048610)
        self.assertDictEqual(track, {
            "source_type": "soundcloud",
            "source_id": 18048610,
            "name": "Sleep Rules Everything Around Me",
            "artists": [
                {
                    "source_type": "soundcloud",
                    "source_id": 5613872,
                    "name": "WUGAZI",
                }
            ],
            "album": None,
            "duration_ms": 199180,
            "preview_url": "https://api.soundcloud.com/tracks/18048610/stream",
            "uri": "soundcloud:song.18048610",
            "track_number": 0,
            "image_small": "https://i1.sndcdn.com/artworks-000008722839-oyzy1n-t67x67.jpg?debc7fd",
            "image_medium": "https://i1.sndcdn.com/artworks-000008722839-oyzy1n-t300x300.jpg?debc7fd",
            "image_large": "https://i1.sndcdn.com/artworks-000008722839-oyzy1n-t500x500.jpg?debc7fd",
        })

    def test_invalid_lookup(self):
        """Soundcloud: Looking up an invalid track raises the appropriate error
        """
        with self.assertRaises(TrackNotFound):
            self.client.lookup_track('asfasfasfas')


class SearchTests(unittest.TestCase):

    def setUp(self):
        load_config()
        self.client = SoundcloudClient(os.environ['SOUNDCLOUD_CLIENT_ID'])

    def test_search_returns_results(self):
        """Soundcloud: Test that search results are returned
        in the correct format.
        """
        results = self.client.search_tracks('wugazi')
        self.assertGreater(len(results), 0)


class FetchAssociatedTrackTests(unittest.TestCase):

    def setUp(self):
        load_config()
        self.client = SoundcloudClient(os.environ['SOUNDCLOUD_CLIENT_ID'])

    def test_fetch_returns_result(self):
        """Youtube: Test that a fetch, returns a random track.
        """
        track_id = '18048610'
        track = self.client.fetch_associated_track(track_id)

        self.assertNotEqual(track['source_id'], track_id)
