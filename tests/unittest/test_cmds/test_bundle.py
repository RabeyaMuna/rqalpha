import os
from unittest import TestCase
from unittest.mock import patch

from rqalpha.cmds.bundle import get_exactly_url


class GetExactlyUrlTestCase(TestCase):
    @patch.dict(os.environ, {"RQALPHA_BUNDLE_DATE": "202508"}, clear=True)
    @patch("rqalpha.cmds.bundle.requests.get")
    def test_pinned_bundle(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = {"content-length": "123"}

        url, total_length = get_exactly_url()

        self.assertEqual(
            url,
            "http://bundle.assets.ricequant.com/bundles_v4/rqbundle_202508.tar.bz2",
        )
        self.assertEqual(total_length, 123)
        mock_get.assert_called_once_with(
            url,
            stream=True,
            proxies={"http": None, "https": None},
        )

    @patch.dict(os.environ, {"RQALPHA_BUNDLE_DATE": "202513"}, clear=True)
    @patch("rqalpha.cmds.bundle.requests.get")
    def test_invalid_pinned_bundle_date(self, mock_get):
        with self.assertRaisesRegex(ValueError, "YYYYMM"):
            get_exactly_url()

        mock_get.assert_not_called()

    @patch.dict(os.environ, {"RQALPHA_BUNDLE_DATE": "202508"}, clear=True)
    @patch("rqalpha.cmds.bundle.requests.get")
    def test_unavailable_pinned_bundle(self, mock_get):
        mock_get.return_value.status_code = 404

        with self.assertRaisesRegex(RuntimeError, "rqbundle_202508"):
            get_exactly_url()
