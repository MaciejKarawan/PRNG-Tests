import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Tests import *
from transforms import *
import itertools

numbers_info = pd.read_pickle('F:/Pulpit_storage/STUDIA/sem7/MonteCarlo/Generatory/Outputs/rc4_1048576.pkl')
prng, n, key, numbers, m = numbers_info['PRNG'], numbers_info['n'], numbers_info['key'], numbers_info['numbers'], numbers_info['Modulus']

print(f'Analysis of: {prng}\n'
      f'Number of numbers: {n}\n'
      f'Key: {key}\n'
      f'M: {m}\n'
      f'Type: Int')

#types
binary_numbers = int_to_binary(numbers, 32)
float_numbers = int_to_float(numbers, 32)


#plt.scatter(numbers, np.ones_like(numbers))
#plt.hist(numbers,bins=32, color = 'c', ec='black', alpha=0.5)
#plt.show()

# Kolmogorov-Smirnov
p1 = KS_test(float_numbers)
print(f'P-value of KS: {p1}')

# Kolmogorov - Smirnov second level
chunks = 10000
splitted = split(float_numbers, chunks)
p12 = KS_test_second_level(splitted)
second_level = chi2_second_level(p12)
print(f'P-value of second level for Kolmogorov-Smirnov: {second_level}')


# Chi2_test_standard
p2 = chi2_test_standard(numbers, 32)
print(f'P-value of chi2: {p2}')

# Chi2_test_standard second-level
chunks = 10000
splitted = split(numbers, chunks)
p22 = chi2_test_standard_second_level(splitted, 32)
second_level = chi2_second_level(p22)
print(f'P-value of second level for Chi2: {second_level}')


# Poker test
fives = (n // 5) * 5
p3 = poker_test(numbers[:fives], 32)
print(f'P-value of poker test: {p3}')
nums=[100, 1000, 5000, 10000]
for i in range(4):
      p = poker_test(numbers[:nums[i]], 32)
      print(f'P-value of poker test: {p} for {nums[i]} first numbers!')

# Frequency monobit
p4 = frequency_monobit(binary_numbers)
print(f'P-value of frequency monobit test: {p4}')

# Frequency second-level
chunks = 50000
number_of_chunks = len(binary_numbers) // chunks
p42 = frequency_monobit_second_level(binary_numbers[:(chunks*number_of_chunks)], chunks)
second_level = chi2_second_level(p42)
print(f'P-value of second level for frequency monobit: {second_level}')


# Birthday spacing test
p5 = birthday_spacing_test(numbers, 32)
print(f'P-value of birthday spacing test: {p5}')

# Birthday spacing second-level
p52 = birthday_spacing_second_level(numbers, 32)
second_level = chi2_second_level(p52)
print(f'P-value of second level for birthday spacing: {second_level}')


fig, axs = plt.subplots(2, 3, sharex = True)
fig.suptitle('Rozkład liczb (RC4)', size=15)

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


axs[1].set_title('Chi2 second level', fontsize=8, alpha=0.8)
axs[1].get_yaxis().set_visible(False)
#axs[0][1].get_xaxis().set_ticks([0.0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
axs[1].scatter(p22, np.ones_like(p22), color='deepskyblue', alpha=0.9)
axs[1].grid(axis='x', color='midnightblue', alpha=0.3)


axs[2].set_title('Frequency monobit second level', fontsize=8, alpha=0.8)
axs[2].get_yaxis().set_visible(False)
#ax.get_xaxis().set_ticks([0.0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
axs[2].scatter(p42, np.ones_like(p42), color='deepskyblue', alpha=0.9)
axs[2].grid(axis='x', color='midnightblue', alpha=0.3)

axs[3].set_title('Birthday spacing second level', fontsize=8, alpha=0.8)
axs[3].get_yaxis().set_visible(False)
#ax.get_xaxis().set_ticks([0.0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
axs[3].scatter(p52, np.ones_like(p52), color='deepskyblue', alpha=0.9)
axs[3].grid(axis='x', color='midnightblue', alpha=0.3)

plt.tight_layout()
plt.show()





