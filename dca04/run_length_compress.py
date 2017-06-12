from bit_io import BitWriter


def encode_data(data, n_bits_for_run_length_encoding):
    current_mode = '0'
    counter = 0
    for i in data:
        if i == current_mode:
            counter += 1
            if counter == 2 ** n_bits_for_run_length_encoding - 1:
                yield counter
                current_mode = '1' if current_mode == '0' else '0'
                counter = 0
        else:
            yield counter
            current_mode = '1' if current_mode == '0' else '0'
            counter = 1
    if counter != 0:
        yield counter


def compress(input_file, output_file, n_bits_for_run_length_encoding):
    with open(input_file, 'r') as f:
        data_to_compress = f.read()
    encoded_data = encode_data(data_to_compress, n_bits_for_run_length_encoding)

    encoded_bits = 0
    bits_used_to_encode = 0
    with open(output_file, 'w') as f:
        bit_writer = BitWriter(f)
        for i in encoded_data:
            bit_writer.write(i, n_bits_for_run_length_encoding)
            encoded_bits += i
            bits_used_to_encode += n_bits_for_run_length_encoding

        bit_writer.flush()
        print "Compression rate: %1.2f" % (float(encoded_bits) / bits_used_to_encode)