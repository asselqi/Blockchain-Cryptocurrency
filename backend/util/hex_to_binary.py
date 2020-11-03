from backend.util.crypto_hash import crypto_hash

HEX_TO_BINARY_CONVERSION_TABLE = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
}

def hex_to_binary(hex_string):
    binary_string = ''
    for char in hex_string:
        binary_string += HEX_TO_BINARY_CONVERSION_TABLE[char]
    return binary_string

def main():
    number = 451
    hex_number = hex(number)
    binary_string = hex_to_binary(hex_number[2:])
    print(f'hex number: {hex_number}')
    print(f'binary number: {binary_string}')
    dec_number = int(binary_string, 2)
    print(f'decimal number: {dec_number}')

    hex_to_binary_crypto_hash = hex_to_binary(crypto_hash('test-data'))
    print(f'hex to binary crypto hash: {hex_to_binary_crypto_hash}')
if __name__ == '__main__':
    main()