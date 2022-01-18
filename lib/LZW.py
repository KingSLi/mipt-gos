class LZWCompressor(object):
    """
    https://neerc.ifmo.ru/wiki/index.php?title=Алгоритм_LZW
    """

    def to_bin_value(self, value):
        return bin(value)[2:]

    def cast_to_bytes(self, value, bit_width):
        bin_value = self.to_bin_value(value)
        return '0' * (bit_width - len(bin_value)) + bin_value

    def compress(self, data):
        dictionary = {bytes([i]): i for i in range(256)}
        max_index = 256
        bit_width = 9
        string = bytes()
        packed_bytes = ""

        for symbol in data:
            curr_byte = bytes([symbol])
            if string + curr_byte in dictionary:
                string += curr_byte
            else:
                # Добавляем в таблицу строк строка + символ, чтобы размер = bit_width
                packed_bytes += self.cast_to_bytes(dictionary[string], bit_width)
                dictionary[string + curr_byte] = max_index
                if len(self.to_bin_value(max_index)) > bit_width:
                    bit_width += 1

                max_index += 1
                string = curr_byte

        packed_bytes += self.cast_to_bytes(dictionary[string], bit_width)
        if len(packed_bytes) % 8 != 0:
            packed_bytes += '0' * (8 - len(packed_bytes) % 8)

        result = bytearray()
        for symbol in range(0, len(packed_bytes), 8):
            result.append(int(packed_bytes[symbol: symbol + 8], 2))
        return result

    def decompress(self, data):
        dictionary = {i: bytes([i]) for i in range(256)}
        next_index = 256
        bit_width = 9
        position = 0
        result = bytearray()

        data_bin_str = ''.join([self.cast_to_bytes(i, 8) for i in data])
        key = int(data_bin_str[position:position + bit_width], 2)
        sequence = dictionary[key]
        result.extend(sequence)
        position += bit_width

        while position + bit_width <= len(data_bin_str):
            key = int(data_bin_str[position:position + bit_width], 2)
            current = dictionary.get(key, sequence + bytes([sequence[0]]))
            result.extend(current)

            dictionary[next_index] = sequence + bytes([current[0]])

            next_index += 1
            position += bit_width
            if len(self.to_bin_value(next_index)) > bit_width:
                bit_width += 1
            sequence = current

        return result
