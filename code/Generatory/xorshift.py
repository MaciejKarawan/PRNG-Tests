import numpy as np
import argparse
import pickle
import time

def ParseArguments():
    parser = argparse.ArgumentParser(description="PRNG")
    parser.add_argument('--n', type=int, default=100, help='Number of generated numbers')
    parser.add_argument('--seed', type=int, default=time.time(), help='initial value')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.seed, args.output_file


def xorshift(n, seed):
    result = []
    result.append(seed)

    for i in range(1, n):
        seed ^= (seed << 13) & 0xFFFFFFFF
        seed ^= (seed >> 17) & 0xFFFFFFFF
        seed ^= (seed << 5) & 0xFFFFFFFF

        result.append(seed)


    return np.array(result)

n, seed, output_file = ParseArguments()
generator = xorshift(n, seed)


if output_file == "":
    print("Wygenerowane liczby: \n", generator)
else:
    data = {'PRNG': 'xorshift',
            'seed': seed,
            'n': n,
            'numbers': generator}

    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)
    print("Generated numbers saved in: ", output_file)