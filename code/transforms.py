import numpy as np

def int_to_binary(numbers, m=32):
    k = np.log2(m)

    if k != np.floor(k):
        raise ValueError('M should be power of 2!')

    k = int(k)
    result = numbers.reshape(len(numbers), 1)
    result = np.array(np.unpackbits(np.array(result, dtype='>i8').view(np.uint8), axis=1), dtype=int)

    return np.ravel(result[:,64-k:])

def float_to_int(numbers, m=32):
    result = np.floor(numbers*m)
    return np.array(result, dtype=int)

def int_to_float(numbers, m):
    return numbers/m

def float_to_binary(numbers):
    return int_to_binary(float_to_int(numbers))

