import math
import numpy as np
import argparse
import pickle
import time


m = 32
time = time.time()
time = str(time).replace('.', '')
k_default = list(map(int, time))

def ParseArguments():
    parser = argparse.ArgumentParser(description="PRNG")
    parser.add_argument('--n', type=int, default=1000, help='Number of generated numbers')
    parser.add_argument('--k', help='key',nargs='+',default=k_default,required=False)
    parser.add_argument('--m', help='Modulus', default=32)
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.k, args.output_file,args.m


def ksa(K, M):
    L = len(K)
    S = list(range(M))
    j = 0

    for i in range(M):
        j = (j + S[i] + int(K[i % L])) % M
        S[i], S[j] = S[j], S[i]

    return S


def prga(S, M, n):
    i = 0
    j = 0

    result = np.empty(n, dtype=int)

    for z in range(n):
        i = (i + 1) % M
        j = (j + S[i]) % M
        S[i], S[j] = S[j], S[i]

        x = S[(S[i] + S[j]) % M]
        result[z] = x

    return result


generator=[]
if isinstance(key, list):
    l=len(key)
    n_split = math.floor(n / l)

    for i in key[0:(l-1)]:
        generator.extend(rc4(np.binary_repr(int(i)),n_split,m))
    generator.extend(rc4(np.binary_repr(int(key[l-1])), n-(l-1)*n_split, m))
else:
    generator = rc4(key, n,m)


if output_file == "":
    print("Wygenerowane liczby: \n", generator)
else:
    data = {'PRNG': 'RC4',
            'key': key,
            'n': n,
            'numbers': generator,
            'Modulus':m}

    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)
    print("Generated numbers saved in: ", output_file)
