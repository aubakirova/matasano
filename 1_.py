def convert_hex(input):
    return input.decode("hex").encode("base64")

def test_convert_hex():
    if convert_hex('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d') == 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t\n':
        print('Success')
    else:
        print('Fail in test_convert_hex')

if __name__ == "__main__":
    test_convert_hex()

