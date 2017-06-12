from unittest import TestCase
from dca04.run_length_compress import encode_data


class TestEncodeData(TestCase):
    def test_encode_data_trivial(self):
        actual = list(encode_data("01", 3))
        self.assertEquals(actual, [1, 1])

    def test_encode_data_empty(self):
        actual = list(encode_data("", 3))
        self.assertEquals(actual, [])

    def test_encode_data_starting_from_wrong_mode(self):
        actual = list(encode_data("1", 3))
        self.assertEquals(actual, [0, 1])

    def test_encode_data_with_sequence_more_than_max_run_length(self):
        actual = list(encode_data("00000000", 3))
        self.assertEquals(actual, [7, 0, 1])

    def test_encode_data_with_big_sequence(self):
        actual = list(encode_data("11111110000000011001010", 3))
        self.assertEquals(actual, [0, 7, 7, 0, 1, 2, 2, 1, 1, 1, 1])

    def test_encode_data_with_big_max_run_length(self):
        actual = list(encode_data("11111110000000011001010", 30))
        self.assertEquals(actual, [0, 7, 8, 2, 2, 1, 1, 1, 1])
