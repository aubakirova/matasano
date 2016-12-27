import array
import re

def convert_hex(input):
    return input.decode("hex").encode("base64")

def test_convert_hex():
    x = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    result = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t\n'
    assert_(convert_hex(x), result)

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
    e = '746865206b696420646f6e277420706c6179'
    assert_(xor(x,y), e)

def single_byte_xor(encoded):
    # Find the message, given that the key is one character long
    byte_array = array.array('B', encoded.decode('hex'))
    best = (0.0, '', '')
    for key in xrange(0,256):
        try:
            tmp = [key ^ b for b in byte_array]
            result_array = "".join("{:c}".format(b) for b in tmp)
            if not re.match("^[\w '-?!.,:;()&]+$", result_array):
                continue
            score = sum([1 if ch.isalpha() else 0 for ch in result_array])
            if score > best[0]:
                best = (score, result_array, key)
        except:
            pass
    # as it turns out, best is "Cooking MCs like a pound of bacon"
    return best

def read_file(name):
    f = open('files/' + name, 'r')
    return f

def detect_single_line():
    filename = '4.txt'
    f = read_file(filename)
    # let's keep 3 best sentences
    best = [(0.0, '', '')] * 3
    def sort_score(t):
        return -t[0]
    for line in f:
        if line[-1] == '\n':
            line = line[:-1]
        current = single_byte_xor(line)
        tmp = sorted(best + [current], key=sort_score)
        best = tmp[:-1]
    # print best
    return best[0]

def test_detect_single_line():
    actual = detect_single_line()
    expected = 'Now that the party is jumping\n'
    assert_(actual[1], expected)

def test_single_byte_xor():
    actual = single_byte_xor('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
    expected = "Cooking MC's like a pound of bacon"
    assert_(actual[1], expected)

def assert_(actual, expected):
    if actual == expected:
        print('Success')
    else:
        print('Failure: expected %s, but got %s' % (expected, actual))

def tests():
    test_convert_hex()
    test_xor()
    test_single_byte_xor()
    test_detect_single_line()

if __name__ == "__main__":
    tests()
    detect_single_line()

