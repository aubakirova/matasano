import array
import base64
import operator
from utils import assert_
from ex1 import edit_distance, single_byte_xor_helper

def decode():
    f = open("files/set1ch6.txt", 'r+')
    # transform file to remove line breaks
    text = f.read()
    text = text.replace('\n', '')
    # print("text", text)
    f.seek(0)
    f.write(text); f.close()
    f = open("files/set1ch6.txt", 'rb')
    keys = most_possible_keysizes(f)
    print("possible keysizes", keys)
    print("keys",  [find_key(key, f) for key in keys])

def find_key(keysize, f):
    blocks = []
    while True:
        b = f.read(keysize)
        if not b:
            break
        blocks.append(b)
    transposed = [''] * keysize
    for b in blocks:
        idx = 0
        for ch in b:
            transposed[idx] += ch
            idx += 1
    # print("blocks",  blocks, transposed)
    key = ''
    for b in transposed:
        print ("Current block is", b)
        encoded = bytearray(b)
        key += (single_byte_xor_helper(encoded)[2])
    return key

def most_possible_keysizes(f):
    results = [find_ed(k, f) for k in range(2, 40)]
    # Sort by the edit distance. Choose three smallest of those
    possible_keys = sorted(results, key=operator.itemgetter(0))
    return [key[1] for key in possible_keys[:3]]

def find_ed(keysize, f):
    b1 = f.read(keysize)
    b2 = f.read(keysize)
    # We need to reset file reading for other keysizes
    f.seek(0)
    return (edit_distance(b1, b2)/keysize, keysize)

def tests():
    print("tests")

if __name__ == "__main__":
    # tests()
    decode()
