def assert_(actual, expected):
    if actual == expected:
        print('Success')
    else:
        print('Failure: expected %s, but got %s' % (expected, actual))

def edit_distance(a, b):
	if len(a) > len(b):
		return edit_distance(b, a)
	distances = range(len(a) + 1)
	for i2, c2 in enumerate(b):
		d = [i2  + 1]
		for i1, c1 in enumerate(a):
			if c1 == c2:
				d.append(distances[i1])
			else:
				d.append(1 + min((distances[i1], distances[i1 + 1], d[-1])))
		distances = d
	return distances[-1]

def convert(data):
	return ''.join(format(ord(t), 'b') for t in data)
    # return ''.join(bin(ord(x))[2:] for x in data)

def count(str1, str2):
	a = convert(str1)
	b = convert(str2) 
	if len(a) > len(b):
		a, b = b, a
	sum =  len(b) - len(a)
	# It must be that `a` is shorter in length than `b`
	# Now we need to make sure that `b` is padded.
	b = b[len(b) - len(a):]	
	for i1, ch1 in enumerate(a):
		if ch1 != b[i1]:
			sum += 1
	return sum 

def test_edit_distance():
	a = convert('this is a test')
	b = convert('wokka wokka!!!')
	assert_(edit_distance(a, b), 37)

if __name__ == "__main__":
	test_edit_distance()
