from collections import Counter
import png
from bit_io import BitWriter
from huffman import huffman

"""
Structure of the .rle file:
================================
================================
4  bits   n_bits_for_number_encoding
4  bits   n_bits_for_code_length_encoding
16 bits   n_huffman_codes
16 bits   row_length

<n_huffman_codes> times:
    <n_bits_for_number_encoding>      bits      number to be huffman-encoded in binary
    <n_bits_for_code_length_encoding> bits      n_bits_for_code_encoding
    <n_bits_for_code_encoding>        bits      huffman code for the number

<n_rows> times:
    Huffman-encoded run-length data for the row

"""


def run_length_encode(data):
    current_mode = 1
    counter = 0
    for i in data:
        if i == current_mode:
            counter += 1
        else:
            yield counter
            current_mode ^= 1
            counter = 1
    if counter != 0:
        yield counter


def get_n_bits_to_encode(number):
    if number == 0:
        return 1
    count = 0
    while number > 0:
        number = number >> 1
        count += 1
    return count


class EncodingMetadata:
    def __init__(self, **kwargs):
        self.n_huffman_codes = kwargs['n_huffman_codes']
        self.huffman_codes = kwargs['huffman_codes']
        self.n_bits_for_number_encoding = kwargs['n_bits_for_number_encoding']
        self.n_bits_for_code_length_encoding = kwargs['n_bits_for_code_length_encoding']
        self.row_length = kwargs['row_length']


def encode_file(png_file):
    with open(png_file, 'r') as f:
        data = png.Reader(f).asDirect()
        bitmap = data[2]
        counter = Counter()
        encoded_data = []
        for row in bitmap:
            encoded_row = list(run_length_encode(row))
            encoded_data.extend(encoded_row)
            counter.update(encoded_row)
            n_huffman_codes = len(counter.keys())
        huffman_codes = huffman(counter.iteritems())
        max_number = max(number for number in huffman_codes.keys())
        n_bits_for_number_encoding = get_n_bits_to_encode(max_number)
        code_max_length = max(len(code) for code in huffman_codes.values())
        n_bits_for_code_length_encoding = get_n_bits_to_encode(code_max_length)
        row_length = data[0]
        return encoded_data, EncodingMetadata(
            n_huffman_codes= n_huffman_codes, huffman_codes= huffman_codes, n_bits_for_number_encoding= n_bits_for_number_encoding,
            n_bits_for_code_length_encoding= n_bits_for_code_length_encoding, row_length= row_length)


def write_encoded_data(file, encoded_data, encoding_metadata):
    with open(file, 'wb') as f:
        bit_writer = BitWriter(f)
        bit_writer.write(encoding_metadata.n_bits_for_number_encoding, 4)
        bit_writer.write(encoding_metadata.n_bits_for_code_length_encoding, 4)
        bit_writer.write(encoding_metadata.n_huffman_codes, 16)
        bit_writer.write(encoding_metadata.row_length, 16)

        for huffman_entry in encoding_metadata.huffman_codes.iteritems():
            code_int = int(huffman_entry[1], 2)
            n_bits_for_code_encoding = len(huffman_entry[1])

            bit_writer.write(huffman_entry[0], encoding_metadata.n_bits_for_number_encoding)
            bit_writer.write(n_bits_for_code_encoding, encoding_metadata.n_bits_for_code_length_encoding)
            bit_writer.write(code_int, n_bits_for_code_encoding)

        for num in encoded_data:
            huffman_entry = encoding_metadata.huffman_codes[num]
            bit_writer.write(int(huffman_entry, 2), len(huffman_entry))
        bit_writer.flush()


encoded_data, encoding_metadata = encode_file('../resources/A003.png')
write_encoded_data('../resources/A003_encoded.rle', encoded_data, encoding_metadata)
