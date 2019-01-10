import struct
import numpy as np
input_file = open('000001.fc6-1','rb')
try:
	sizes = [struct.unpack('i',input_file.read(4))[0] for i in range(5)]
	m = np.prod(sizes)
	data = [struct.unpack('f',input_file.read(4))[0] for i in range(m)]
finally:
	input_file
feature_vector = np.array(data)

print(feature_vector.shape)
