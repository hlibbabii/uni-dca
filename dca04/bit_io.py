import struct


class BitWriter:
    def __init__(self, file, max_buffer_length=1024 * 8):
        self.file = file
        self.max_buffer_length = max_buffer_length
        self.buffer = []

    def __write_buffer_into_file__(self, bits_to_write):
        i = 0
        bytes = []

        # converting every 8 bits to bytes
        while i + 8 <= bits_to_write:
            value = int("".join(self.buffer[i:i+8]), 2)
            bytes.append(struct.pack('B', value))
            i += 8

        # converting left-over bits appending zeros if necessary
        leftover_bits_count = bits_to_write - i
        if leftover_bits_count > 0:
            value = int("".join(self.buffer[i:i+leftover_bits_count]), 2) << (8 - leftover_bits_count)
            bytes.append(struct.pack('B', value))

        self.file.write(bytearray(bytes))
        del self.buffer[0:bits_to_write]

    def write(self, int_value, n_bits):
        # convert int_value into binary string
        str = ['1' if digit == '1' else '0' for digit in bin(int_value)[2:]]
        if len(str) > n_bits:
            raise ValueError("{0} can't be written into {1} bits".format(int_value, n_bits))
        # add leading zeros
        self.buffer.extend(['0' for i in range(0, n_bits - len(str))])
        # add binary string itself
        self.buffer.extend(str)
        if len(self.buffer) >= self.max_buffer_length:
            self.__write_buffer_into_file__(len(self.buffer) - len(self.buffer) % 8)

    def flush(self):
        if len(self.buffer) > 0:
            self.__write_buffer_into_file__(len(self.buffer))
        self.file.flush()


class BitReader():
    def __init__(self, file):
        self.file = file
        self.buffer = []

    def __fill_the_buffer__(self, n_bits):
        n_bytes_to_read = n_bits / 8 + 1
        bytes = bytearray(self.file.read(n_bytes_to_read))
        for b in bytes:
            self.buffer.extend(bin(b)[2:].zfill(8))

    def read(self, n_bits):
        if len(self.buffer) < n_bits:
            self.__fill_the_buffer__(n_bits)
        if len(self.buffer) > 0:
            str = "".join(self.buffer[0:n_bits])
            del self.buffer[0:n_bits]
            return int(str, 2)
        else:
            raise ValueError()

    def read_all(self, n_bits):
        try:
            while True:
                yield self.read(n_bits)
        except:
            pass

