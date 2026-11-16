import numpy as np
from math import sqrt, erf, floor
from scipy.stats import chi2, norm
import pandas as pd
from scipy.stats import chisquare, norm, chi2_contingency
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.special import kolmogorov
from transforms import int_to_float,int_to_binary
from monobit_frequency_test import frequency_monobit
from KS_test import KS_test
from chi_square_test import chi2_test,chi2_test_standard
import runs_test
GLCG = pd.read_pickle('generated_numbers_GLCG.pkl')

GLCG_numbers = GLCG['numbers']
print(len(GLCG_numbers))
GLCG_numbers=np.array(GLCG_numbers)
M_GLCG= GLCG['Modulus']
n_GLCG=int(GLCG['n'])
#print(GLCG_numbers[:10])
print(n_GLCG)


u_GLCG=int_to_float(GLCG_numbers,M_GLCG)
print("UNIFORM GLCG", u_GLCG[:6])

def frequency_test(p_values, M=100): #zliczanie wartości w koszykach
    p_i = 1 / M
    N=len(p_values)
    E_i=N*p_i
    count_observations=p_values.groupby(pd.cut(p_values['val'], np.arange(0, 1 + p_i, p_i),include_lowest=True),observed=False).count()
    return(count_observations)
print("Rozkład wartości na {0,...,M-1}",Counter(GLCG_numbers),"Ile różnych wartości",len(np.unique(GLCG_numbers)))
#rozkład wartości na koszyki
buckets_count=frequency_test(pd.DataFrame({'val':u_GLCG}),M=250)
print("Jednostajny podział wartości:",buckets_count)
def split_list(list, chunk_size):
    for i in range(0, len(list), chunk_size):
        yield list[i:i + chunk_size]
def p_values(generator,m=None,chunk_size=1024,test=chi2_test_standard):
    data = list(split_list(generator,chunk_size))
    p_values = []
    if m == None:
        for i in data:
            p_values.append(test(i))
    else:
        for i in data:
            p_values.append(test(i,m))
    return p_values


print("Kołogomorov Smirnow", KS_test(u_GLCG))
ks_pval=p_values(u_GLCG,test=KS_test)
print("Kołogomorow Smirnov p wartosci gdy dzielimy wygenerowane liczby na chunki",ks_pval)

print("chi kwadrat dla GLCG",chi2_test_standard(GLCG_numbers,m=M_GLCG))
chi_pval_GLCG=p_values(GLCG_numbers,1024)
print("P wartości dla chi kwadrat, gdy dzielimy wygenerowane liczby na chunki:\n",chi_pval_GLCG)

freq_KS_GLCG_pval=pd.DataFrame(frequency_test(pd.DataFrame({'val':ks_pval}),M=10))
freq_test_GLCG_pval=pd.DataFrame(frequency_test(pd.DataFrame({'val':chi_pval_GLCG}),M=10))

print("Rozkład p_wartości z KS jednostajny?\n", freq_KS_GLCG_pval[freq_KS_GLCG_pval['val']>0])
print("Rozkład p_wartości z chi2 jednostajny?\n", freq_test_GLCG_pval[freq_test_GLCG_pval['val']>0])




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





bin_GLCG=int_to_binary(np.array(GLCG_numbers),10)
print("runs test GLCG: ",runs_test(bin_GLCG))
print("frequency_monobit",frequency_monobit(bin_GLCG))
GLCG_obs=np.array(list(freq_test_GLCG_pval['val']))
GLCG_exp=np.array([sum(GLCG_obs)/len(GLCG_obs)]*len(GLCG_obs))

print("Chi dla p_val: ",chi2_test(GLCG_obs,GLCG_exp))


GLCG_pairs=[[GLCG_numbers[i] , GLCG_numbers[2*i]] for i in range(0,int(n_GLCG/2))]
plt.style.use('ggplot')
plt.hist(GLCG_numbers,color='pink',bins=128,edgecolor='blue', label=GLCG['PRNG'])
plt.title(f'Histogram dla '+ str(GLCG['PRNG'] ))
plt.xlabel('Wartość')
plt.ylabel('Częstość')
plt.legend()
plt.show()


plt.plot(GLCG_pairs[:1000], label=GLCG['PRNG'])
plt.title(f'Histogram dla '+ str(GLCG['PRNG'] ))
plt.xlabel('Wartość')
plt.ylabel('Częstość')
plt.legend()
plt.show()
