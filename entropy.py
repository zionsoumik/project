from __future__ import division
from collections import Counter

import math
l=[]
entropy_list=[]
with open("train.txt") as filename:
    for line in filename:
        l.append(tuple(float(x) for x in line.strip().split()))
mydict=Counter(x[:-1] for x in l)
g=list(mydict.keys())
for num1 in range(0,len(g[1])):
    h=[]
    for x in g:
        h.append(x[num1])
    h=sorted(h)
    pk=[]
    bar=0
    j=0
    for i in range(0,int(len(l)/10)):
        bar=bar+10/len(l)
        count=0
        while j<len(h):
            if h[j]<bar:
                count+=1
                j+=1
            else:
                break
        pk.append(count)
    num_zero=0
    entropy=0
    for p in pk:
        if p!=0:
            entropy+=p/len(l)*math.log(p/len(l),2)
        else:
            num_zero+=1
    entropy=(num_zero-1)/(2*len(l)*math.log(2))-entropy
    print(entropy)
    entropy_list.append(entropy)
total=sum(entropy_list)
bin=[]
for e in entropy_list:
    bin.append(math.pow(10000,e/total))
print(bin)