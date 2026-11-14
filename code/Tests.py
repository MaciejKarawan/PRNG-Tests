import numpy as np
from scipy.stats import norm
from scipy.stats import chisquare, poisson
from scipy.special import kolmogorov
from math import prod
from stirling import s2

def split(numbers, chunks):
    n = len(numbers)
    number_of_chunks = n // chunks
    max_value = number_of_chunks*chunks

    return np.array(np.split(numbers[:max_value], number_of_chunks))


def frequency_monobit(numbers):
    x = 2*numbers - 1
    s = x.cumsum()
    t = abs(s[-1]/np.sqrt(len(x)))
    p = 2*(1 - norm().cdf(t))

    return p

#second-level
def frequency_monobit_second_level(numbers, block):
    n = len(numbers)
    num_of_blocks = int(n / block)
    test = np.array([numbers[i*block:(i+1)*block] for i in range(num_of_blocks)])

    ps = []

    for i in range(num_of_blocks):
        p = frequency_monobit(test[i,])
        ps.append(p)

    return np.array(ps)


def chi2_test(obs, expctd): # numpy arrays arguments

    if expctd.size == 0 or expctd.size != obs.size:
        raise ValueError('Incorrect length of expected outcomes!')

    chi_stat, p_value = chisquare(obs, expctd)

    return p_value


def chi2_test_standard(numbers, m): #m - exclusive number of balls

    unique = np.unique(numbers, return_counts=True)
    obs = unique[1]
    n = len(obs)

    if n < m:
        obs = np.concatenate((obs, np.zeros(m-n)))

    expected = np.zeros_like(obs) + (len(numbers)/len(obs))

    return chi2_test(obs, expected)

def chi2_test_standard_second_level(numbers, m): # Test dzielący liste i wykonujący chi2_standard dla podzielonych list
    number_of_chunks = len(numbers)
    ps = []

    for i in range(number_of_chunks):
        p = chi2_test_standard(numbers[i], m)
        ps.append(p)

    return np.array(ps)

def chi2_second_level(ps): # Test dla już p-wartości
    n = len(ps)
    obs = []

    for i in range(10):
        lower_bound = i*0.1
        upper_bound = (i+1)*0.1
        obs.append(sum(np.vectorize(lambda x: lower_bound <= x <= upper_bound)(ps)))

    expctd = np.ones(10, dtype=int)*(0.1 * n)
    obs = np.array(obs)

    return chi2_test(obs, expctd)

def KS_test(numbers):
    d_plus = []
    d_minus = []
    n = len(numbers)
    testing = numbers.copy()
    testing.sort()

    for i in range(1, n + 1):

        x = i/n - testing[i - 1]
        d_plus.append(x)

        y = testing[i - 1] - (i-1)/n
        d_minus.append(y)

    D_n = max(max(d_plus), max(d_minus))
    D_k = np.sqrt(n)*D_n + 1/(np.sqrt(n)*6) + (np.sqrt(n)*D_n -1)/(4*n)
    p = 1 - kolmogorov(D_k)

    return(p)

def KS_test_second_level(numbers):
    number_of_chunks = len(numbers)
    ps = []

    for i in range(number_of_chunks):
        p = KS_test(numbers[i])
        ps.append(p)

    return np.array(ps)

# int, m, n = 5r

def poker_test(numbers, m):
    n = len(numbers)
    number_of_fives = n/5

    if number_of_fives != np.floor(number_of_fives):
        raise ValueError('Length of sequence of numbers should be multiplication of 5!')

    number_of_fives = int(number_of_fives)
    transformed = np.array([numbers[5*i:5*(i+1)] for i in range(number_of_fives)])
    ps = np.array([prod(range(m-i+1, m+1))*s2(5, i)/(m**5) for i in range(1, 6)])
    o1, o2, o3, o4, o5 = 0, 0, 0, 0, 0

    for i in range(number_of_fives):
        counts = np.unique(transformed[i], return_counts=True)[1]
        max_count = max(counts)

        if max_count == 1:
            o5 += 1
        elif max_count == 2:
            o4 += 1
        elif max_count == 3:
            o3 += 1
        elif max_count == 4:
            o2 += 1
        elif max_count == 5:
            o1 += 1

    os = np.array([o1, o2, o3, o4, o5])
    return chi2_test(os, ps*number_of_fives)


def poker_test_second_level(numbers, m):
    number_of_chunks = len(numbers)
    ps = []

    for i in range(number_of_chunks):
        p = poker_test(numbers[i], m)
        ps.append(p)

    return np.array(ps)


def birthday_spacing_test(numbers,m): #Modulo
    n=len(numbers)
    numbers_sorted=np.sort(numbers)
    lambda1=n**3/(4*m)
    S=[numbers_sorted[i+1]-numbers_sorted[i] for i in np.arange(0,n,2)]
    K=0

    for i in set(S):
        K=+(S.count(i)-1)

    return 1-poisson.cdf(k=K-1,mu=lambda1)


def birthday_spacing_second_level(numbers, m): #block size should be int((8*modulus)**(1/3))
    n = len(numbers)
    block=int((8*m)**(1/3))
    num_of_blocks = int(n / block)
    test = np.array([numbers[i*block:(i+1)*block] for i in range(num_of_blocks)])

    ps = []

    for i in range(num_of_blocks):
        p = birthday_spacing_test(test[i,],m)
        ps.append(p)

    return np.array(ps)