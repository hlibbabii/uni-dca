from io import FileIO
from unittest import TestCase
import mock
from bit_io import BitWriter, BitReader


class TestBitWriter(TestCase):
    def testWrite1(self):
        mocked_file = mock.create_autospec(FileIO)
        bit_writer = BitWriter(mocked_file, 4)
        bit_writer.write(32, 8)
        bit_writer.flush()

        mocked_file.write.assert_called_with(bytearray(b'\x20'));
        mocked_file.flush.called

    def testWrite2(self):
        mocked_file = mock.create_autospec(FileIO)
        bit_writer = BitWriter(mocked_file, 4)
        bit_writer.write(255, 8)
        bit_writer.flush()

        mocked_file.write.assert_called_with(bytearray(b'\xff'));
        mocked_file.flush.called

    def testWrite3(self):
        mocked_file = mock.create_autospec(FileIO)
        bit_writer = BitWriter(mocked_file, 4)
        bit_writer.write(1, 2)
        bit_writer.write(1, 2)
        bit_writer.flush()

        mocked_file.write.assert_called_with(bytearray(b'\x50'));
        mocked_file.flush.called


class TestBitReader(TestCase):
    def testRead1(self):
        mocked_file = mock.create_autospec(FileIO)
        mocked_file.read.side_effect = [[b'\xff']]

        bitReader = BitReader(mocked_file)
        actual = list(bitReader.read(4))

        self.assertEquals(actual, [15, 15])

    def testRead1(self):
        mocked_file = mock.create_autospec(FileIO)
        mocked_file.read.side_effect = [[b'\xff'], [b'\x00']]

        bitReader = BitReader(mocked_file)
        actual = list(bitReader.read(2))

        self.assertEquals(actual, [3, 3, 3, 3, 0, 0, 0, 0])