from __future__ import print_function, unicode_literals
import unittest
import sprengel


class EncodePathTest(unittest.TestCase):
    def _assert_encode_path(self, filename, expected):
        self.assertEqual(expected, sprengel.encode_path(filename))

    def test_returns_string(self):
        self._assert_encode_path(b"abc", "abc")

    def test_replaces_underscore(self):
        self._assert_encode_path(b"o_o", "o__o")

    def test_replaces_uppercase(self):
        self._assert_encode_path(b"xA", "x_a")

    def test_replaces_non_ascii(self):
        self._assert_encode_path(b"x\xce", "x~ce")

    def test_replaces_tilde(self):
        self._assert_encode_path(b"x~", "x~7e")


if __name__ == "__main__":
    unittest.main()
