from backend.util.hex_to_binary import hex_to_binary

def test_hex_to_binary():
    number = 451
    hex_number = hex(number)
    binary_string = hex_to_binary(hex_number[2:])
    dec_number = int(binary_string, 2)
    assert dec_number == number
    for i in range(1000000):
        hex_number = hex(i)
        binary_number = hex_to_binary(hex_number[2:])
        decimal_number = int(binary_number, 2)
        assert decimal_number == i

