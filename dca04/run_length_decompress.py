from bit_io import BitReader


def decode_data(encoded_data):
    current_mode = '0'
    for d in encoded_data:
        yield current_mode * d
        current_mode = '1' if current_mode == '0' else '0'


def decompress(input_file, output_file, n_bits_for_run_length_encoding):
    with open(input_file, 'r') as f:
        bit_reader = BitReader(f)
        decoded_data = decode_data(bit_reader.read(n_bits_for_run_length_encoding))

        with open(output_file, 'w') as w:
            for i in decoded_data:
                w.write(i)
