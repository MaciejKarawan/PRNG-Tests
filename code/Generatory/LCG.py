import numpy as np
import argparse
import pickle
import time


def ParseArguments():
    parser = argparse.ArgumentParser(description="PRNG")

    parser.add_argument('--n', type=int, default=100, help='Number of generated numbers')
    parser.add_argument('--seed', type=int, default=int(time.time()), help='initial value')
    parser.add_argument('--m', type=int, help='Modulo')
    parser.add_argument('--a', type=int, default=1, help='coefficient a')
    parser.add_argument('--c', type=int, default=5, help='coefficient c')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.seed, args.m, args.a, args.c, args.output_file


def lcg(n, seed, M, a, c):
    result = np.empty(n, dtype=int)
    result[0] = int(seed % M)

    for i in range(1, n):
        result[i] = (a * result[i - 1] + c) % M

    return result


n, seed, m, a, c, output_file = ParseArguments()

generator = lcg(n, seed, m, a, c)

if output_file == "":
    print("Wygenerowane liczby: \n", generator)
else:
    data = {'PRNG': 'LCG',
            'a': a,
            'c': c,
            'Modulus': m,
            'n': n,
            'numbers': generator}

    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)
    print("Generated numbers saved in: ", output_file)
