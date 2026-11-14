import numpy as np
from math import sqrt, erf, floor
from scipy.stats import chi2, norm
import pandas as pd
from scipy.stats import chisquare, norm, chi2_contingency
from collections import Counter
import matplotlib.pyplot as plt
from scipy.special import kolmogorov
from transforms import int_to_float,int_to_binary
from monobit_frequency_test import frequency_monobit
from KS_test import KS_test
from chi_square_test import chi2_test,chi2_test_standard
import runs_test

LCG = pd.read_pickle('generated_numbers_LCG.pkl')

LCG_numbers = LCG['numbers']
LCG_numbers=np.array(LCG_numbers)
M_LCG= LCG['Modulus']
n_LCG=int(LCG['n'])
#print(LCG_numbers[:10])
print(n_LCG)


u_LCG=int_to_float(LCG_numbers,M_LCG)
print("UNIFORM LCG", u_LCG[:6])

def frequency_test(p_values, M=100): #zliczanie wartości w koszykach
    p_i = 1 / M
    N=len(p_values)
    E_i=N*p_i
    count_observations=p_values.groupby(pd.cut(p_values['val'], np.arange(0, 1 + p_i, p_i),include_lowest=True),observed=False).count()
    return(count_observations)
print("Rozkład wartości na {0,...,M-1}",Counter(LCG_numbers),"Ile różnych wartości",len(np.unique(LCG_numbers)))
#rozkład wartości na koszyki
buckets_count=frequency_test(pd.DataFrame({'val':u_LCG}),M=250)
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


print("Kołogomorov Smirnow", KS_test(u_LCG))
ks_pval=p_values(u_LCG,test=KS_test)
print("Kołogomorow Smirnov p wartosci gdy dzielimy wygenerowane liczby na chunki",ks_pval)

print("chi kwadrat dla LCG",chi2_test_standard(LCG_numbers,m=M_LCG))
chi_pval_LCG=p_values(LCG_numbers,1024)
print("P wartości dla chi kwadrat, gdy dzielimy wygenerowane liczby na chunki:\n",chi_pval_LCG)

freq_KS_LCG_pval=pd.DataFrame(frequency_test(pd.DataFrame({'val':ks_pval}),M=10))
freq_test_LCG_pval=pd.DataFrame(frequency_test(pd.DataFrame({'val':chi_pval_LCG}),M=10))

print("Rozkład p_wartości z KS jednostajny?\n", freq_KS_LCG_pval[freq_KS_LCG_pval['val']>0])
print("Rozkład p_wartości z chi2 jednostajny?\n", freq_test_LCG_pval[freq_test_LCG_pval['val']>0])




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





bin_LCG=int_to_binary(np.array(LCG_numbers),10)
print("runs test LCG: ",runs_test(bin_LCG))
print("frequency_monobit",frequency_monobit(bin_LCG))
lcg_obs=np.array(list(freq_test_LCG_pval['val']))
lcg_exp=np.array([sum(lcg_obs)/len(lcg_obs)]*len(lcg_obs))

print("Chi dla p_val: ",chi2_test(lcg_obs,lcg_exp))

LCG_pairs=[[LCG_numbers[i] , LCG_numbers[2*i]] for i in range(0,int(n_LCG/2))]
plt.hist(LCG_numbers,color='pink',bins=128,edgecolor='blue', label=LCG['PRNG'])
plt.title(f'Histogram dla '+ str(LCG['PRNG'] ))
plt.xlabel('Wartość')
plt.ylabel('Częstość')
plt.legend()
plt.style.use('ggplot')
plt.show()



plt.plot(LCG_pairs[:1000], label=LCG['PRNG'])
plt.title(f'Wartości dla '+ str(LCG['PRNG'] ))
plt.ylabel('Wartość')
plt.legend()
plt.style.use('ggplot')
plt.show()




plt.hist(chi_pval_LCG, label="P wartości z testu chi kwadrat")
plt.title(f'Wartości dla '+ str(LCG['PRNG'] ))
plt.ylabel('Wartość')
plt.legend()
plt.style.use('ggplot')
plt.show()


plt.hist(ks_pval, label="P wartości z testu Kołogomorowa Smirnova")
plt.title(f'Wartości dla '+ str(LCG['PRNG'] ))
plt.ylabel('Wartość')
plt.legend()
plt.style.use('ggplot')
plt.show()
