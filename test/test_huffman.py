from unittest import TestCase

from huffman import huffman
from huffman_compression import get_n_bits_to_encode


class TestHuffman(TestCase):
    def test_huffman1(self):
        result = huffman([('A', 6), ('B', 7), ('C', 6), ('D', 7), ('E', 1000), ])
        self.assertItemsEqual(result, [('A', '111'), ('C', '110'), ('B', '101'), ('D', '100'), ('E', '0')])

    def test_huffman1(self):
        result = huffman([('A', 10), ('B', 1), ('C', 100)])
        self.assertItemsEqual(result, [('A', '10'), ('B', '11'), ('C', '0')])

    def test_get_n_bits_to_encode1(self):
        self.assertEquals(get_n_bits_to_encode(7), 3)

    def test_get_n_bits_to_encode1(self):
        self.assertEquals(get_n_bits_to_encode(256), 9)