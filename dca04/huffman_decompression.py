import png
from bit_io import BitReader


def extract_data_from_file(file):
    with open(file, 'r') as f:
        bit_reader = BitReader(f)
        n_bits_for_number_encoding = bit_reader.read(4)
        n_bits_for_code_length_encoding = bit_reader.read(4)
        n_huffman_codes = bit_reader.read(16)
        row_length = bit_reader.read(16)

        huffman_codes = {}
        for i in range(n_huffman_codes):
            number = bit_reader.read(n_bits_for_number_encoding)
            bits_for_code = bit_reader.read(n_bits_for_code_length_encoding)
            code_int = bit_reader.read(bits_for_code)
            code = bin(code_int)[2:]
            code = '0' * (bits_for_code - len(code)) + code
            huffman_codes[code] = number

        runs = []
        bit_buffer = ""
        for bit in bit_reader.read_all(1):
            bit_buffer += str(bit)
            if bit_buffer in huffman_codes:
                runs.append(huffman_codes[bit_buffer])
                bit_buffer = ""
        return runs, row_length


def convert_runs_into_bits(runs, row_length):
    bitmap = []
    row = []
    current_mode = 1
    for run in runs:
        row.extend([current_mode for i in range(run)])
        if len(row) > row_length:
            raise AssertionError()
        elif len(row) == row_length:
            bitmap.append(row)
            row = []
            current_mode = 1
        else:
            current_mode ^= 1
    return bitmap


def write_bits_to_png(bits, file):
    with open(file, 'wb') as f:
        w = png.Writer(len(bits[0]), len(bits), greyscale=True, bitdepth=1, gamma=1.0, background=(1,))
        w.write(f, bits)


runs, row_length = extract_data_from_file('../resources/A003_encoded.rle')
bits = convert_runs_into_bits(runs, row_length)
write_bits_to_png(bits, '../resources/A003_decoded.png')
