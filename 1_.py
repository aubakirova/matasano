def convert_hex(input):
    return input.decode("hex").encode("base64")

def test_convert_hex():
    if convert_hex('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d') == 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t\n':
        print('Success')
    else:
        print('Fail in test_convert_hex')

def xor(x, y):
    x_decode = x.decode('hex')
    y_decode = y.decode('hex')
    result = ''
    for a, b in zip(x_decode, y_decode):
        result += chr(ord(a) ^ ord(b))
    return result.encode('hex')

def test_xor():
    x = '1c0111001f010100061a024b53535009181c'
    y = '686974207468652062756c6c277320657965'
    if xor(x, y) == '746865206b696420646f6e277420706c6179':
        print('Success')
    else:
        print('Failure %s' % xor(x, y))

def tests():
    test_convert_hex()
    test_xor()

if __name__ == "__main__":
    tests()

