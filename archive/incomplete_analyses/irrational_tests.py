import numpy as np
from scipy.stats import chisquare
from scipy.stats import norm
import math
def frequency_monobit(numbers):
    x = 2*numbers - 1
    s = x.cumsum()
    t = abs(s[-1]/np.sqrt(len(x)))
    p = 2*(1 - norm().cdf(t))

    return p


def runs_test(numbers):
    n=len(numbers)
    k=sum(numbers)/n
    if abs(k-0.5)>=0.3 :
        p=0
        return(p)
    else:
        V_stat=0
        for i in np.arange(0,n-2):
            if numbers[i]==numbers[i+1] :
                V_stat=+1
    p=math.erfc(abs(V_stat-2*n*k*(1-k)/(2*math.sqrt(2*n)*k*(1-k))))
    return(p)



def transform_file(plik):
    result = []

    for line in plik:
        line = line.strip()
        x = [int(i) for i in line]
        result.extend(x)
    return(result)


with open('data.e.txt', 'r') as plik_e:
    e = transform_file(plik_e)
    print("Rozwiniecie e",e[:10],"\n")
with open('data.pi.txt', 'r') as plik_pi:
    pi = transform_file(plik_pi)
    print("Rozwiniecie pi",pi[:10],"\n")
with open('data.sqrt2.txt', 'r') as plik_sqrt:
    sqrt = transform_file(plik_sqrt)
    print("Rozwiniecie pierwiastka z dwóch",sqrt[:10],"\n")




def bits_to_int(numbers,k=100):

    return(int("".join(str(x) for x in numbers[:k])))



print("PI")
print("monobit",frequency_monobit(np.array(pi)))
print("runs test", runs_test(pi))

print("e")
print("monobit",frequency_monobit(np.array(e)))
print("runs test", runs_test(e))

print("sqrt")

print("monobit",frequency_monobit(np.array(sqrt)))
print("runs test", runs_test(sqrt))