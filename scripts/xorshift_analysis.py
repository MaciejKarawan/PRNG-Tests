from pathlib import Path

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

from prng_tests.metrics import KS_test, KS_test_second_level, birthday_spacing_second_level, birthday_spacing_test, chi2_second_level, frequency_monobit, frequency_monobit_second_level, np, poker_test, poker_test_second_level, split

from prng_tests.transforms import int_to_binary, int_to_float, np

import itertools


def main():
    global GENERATED_DATA, axs, binary_numbers, chunks, fig, fives, float_numbers, i, j, k, m, n, number_of_chunks, numbers, numbers_info, p1, p12, p3, p32, p4, p42, p5, p52, prng, second_level, seed, splitted, z
    GENERATED_DATA = Path(__file__).resolve().parents[1] / "data" / "generated"

    numbers_info = pd.read_pickle(str(GENERATED_DATA / 'xorshift_1048576.pkl'))

    prng, n, seed, numbers = numbers_info['PRNG'], numbers_info['n'], numbers_info['seed'], numbers_info['numbers']

    m = 2**32

    print(f'Analysis of: {prng}\n'
          f'Number of numbers: {n}\n'
          f'seed: {seed}\n'
          f'M: {m}\n'
          f'Type: Int')

    binary_numbers = int_to_binary(numbers, m)

    float_numbers = int_to_float(numbers, m)

    p1 = KS_test(float_numbers)

    print(f'P-value of KS: {p1}')

    chunks = 10000

    splitted = split(float_numbers, chunks)

    p12 = KS_test_second_level(splitted)

    second_level = chi2_second_level(p12)

    print(f'P-value of second level for Kolmogorov-Smirnov: {second_level}')

    fives = (n // 5) * 5

    p3 = poker_test(numbers[:fives], m)

    print(f'P-value of poker test: {p3}')

    chunks = 1000

    p32 = poker_test_second_level(split(numbers, chunks), m)

    second_level = chi2_second_level(p32)

    print(f'P-value of second level for Poker Test: {second_level}')

    p4 = frequency_monobit(binary_numbers)

    print(f'P-value of frequency monobit test: {p4}')

    chunks = 50000

    number_of_chunks = len(binary_numbers) // chunks

    p42 = frequency_monobit_second_level(binary_numbers[:(chunks*number_of_chunks)], chunks)

    second_level = chi2_second_level(p42)

    print(f'P-value of second level for frequency monobit: {second_level}')

    p5 = birthday_spacing_test(numbers, m)

    print(f'P-value of birthday spacing test: {p5}')

    p52 = birthday_spacing_second_level(numbers, m)

    second_level = chi2_second_level(p52)

    print(f'P-value of second level for birthday spacing: {second_level}')

    fig, axs = plt.subplots(2, 3, sharex = True)

    fig.suptitle('Rozkład liczb (XORshift)', size=15)

    k = [50, 100, 500, 1000, 10000, 100000]

    z = 0

    for i, j in itertools.product(range(2), range(3)):
          axs[i][j].hist(numbers[:k[z]], bins=32, color = 'deepskyblue', ec='black', alpha=0.5, align='mid')
          axs[i][j].set_title(f'Pierwsze {k[z]} liczb', size=9)
          axs[i][j].grid(axis='y', color='midnightblue', alpha=0.1, in_layout=True)
          z += 1

    fig, axs = plt.subplots(4, 1, sharex = True)

    fig.suptitle('Rozkład p-wartości', fontsize=15, x=0.5)

    axs[0].set_title('Kolmogorov-Smirnov second level', fontsize=8, alpha=0.8)

    axs[0].get_yaxis().set_visible(False)

    axs[0].get_xaxis().set_ticks([0.0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

    axs[0].scatter(p12, np.ones_like(p12), color='deepskyblue', alpha=0.9)

    axs[0].grid(axis='x', color='midnightblue', alpha=0.3)

    axs[1].set_title('Frequency monobit second level', fontsize=8, alpha=0.8)

    axs[1].get_yaxis().set_visible(False)

    axs[1].scatter(p42, np.ones_like(p42), color='deepskyblue', alpha=0.9)

    axs[1].grid(axis='x', color='midnightblue', alpha=0.3)

    axs[2].set_title('Poker test second level', fontsize=8, alpha=0.8)

    axs[2].get_yaxis().set_visible(False)

    axs[2].scatter(p32, np.ones_like(p32), color='deepskyblue', alpha=0.9)

    axs[2].grid(axis='x', color='midnightblue', alpha=0.3)

    axs[3].set_title('Birthday spacing second level', fontsize=8, alpha=0.8)

    axs[3].get_yaxis().set_visible(False)

    axs[3].scatter(p52, np.ones_like(p52), color='deepskyblue', alpha=0.9)

    axs[3].grid(axis='x', color='midnightblue', alpha=0.3)

    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    main()
