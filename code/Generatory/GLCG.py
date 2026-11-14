import numpy as np
import argparse
import pickle
import time


def ParseArguments():
    parser = argparse.ArgumentParser(description="PRNG")

    parser.add_argument('--n', type=int, default=100, help='Number of generated numbers')
    parser.add_argument('--seeds', nargs='+', type=int, default=[111, 17, 297], help='initial values')
    parser.add_argument('--m', type=int, default=2**10, help='Modulo')
    parser.add_argument('--coef', nargs='+', default=[3,7,68], type=int, help='coefficients')

    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.seeds, args.m, args.coef, args.output_file


n, seeds, m, coef, output_file = ParseArguments()



coef = np.array(coef)
seeds = np.array(seeds)

def glcg(n, seeds, M, coef): # seeds and coef should be numpy arrays
    result = np.empty(n, dtype=int)
    nseeds = len(seeds)

    for i in range(nseeds):
        result[i] = seeds[i]

    for i in range(nseeds, n):
        x = np.dot(seeds, coef) % M
        seeds = np.roll(seeds, 1)
        seeds[0] = x
        result[i] = x

    return result


generator = glcg(n, seeds, m, coef)



if output_file == "":
    print("Wygenerowane liczby: \n", generator)
else:
    data = {'PRNG': 'GLCG',
            'coefficients': coef,
            'Modulus': m,
            'n': n,
            'numbers': generator}

    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)
    print("Generated numbers saved in: ", output_file)
