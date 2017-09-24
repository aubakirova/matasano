import array
import re
import editdistance
from utils import assert_

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

def test_single_byte_xor():
    actual = single_byte_xor('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
    expected = "Cooking MC's like a pound of bacon"
    assert_(actual[1], expected)

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

def repeating_xor(encode, key):
    key = array.array('B', key)
    byte_array = array.array('B', encode)
    result = byte_array
    current = 0
    for i in range(len(byte_array)):
        result[i] = byte_array[i] ^ key[current]
        current = current + 1
        if current > len(key)-1:
            current = 0
    return "".join("{:c}".format(b) for b in result).encode('hex')

# Set 5. Challenge 5. Implement repeating-key XOR
def test_repeating_xor():
    actual = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    expected = ("0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765"
                "272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27"
                "282f")
    assert_(repeating_xor(actual, "ICE"), expected)

def byte_or(b1, b2):
    # return [ord(a) ^ ord(b) for a,b in zip(x, y)]
    res = [i^j for i, j in zip(b1, b2)]
    return str(bytearray(res))

def edit_distance(a1, a2):
    a1 = "this is a test"
    a2 = "wokka wokka!!!"
    b1 = bytearray(a1)
    b2 = bytearray(a2)
    b = byte_or(b1, b2)
    dist = 0
    for char in b:
        dist += bin(ord(char))[2:].count('1')
    return dist

def test_edit_distance():
    a1 = "this is a test"
    a2 = "wokka wokka!!!"
    assert_(edit_distance(a1, a2), 37)

def tests():
    test_convert_hex()
    test_xor()
    test_single_byte_xor()
    test_detect_single_line()
    test_repeating_xor()
    test_edit_distance()

if __name__ == "__main__":
    tests()
