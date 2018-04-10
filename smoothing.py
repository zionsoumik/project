from __future__ import division
from collections import Counter
import csv
import copy
import math
q_bnds=[]
train=[]
filename1=open("eval.txt")
filename=open("train.txt")
for line in filename:
    train.append(tuple(float(x) for x in line.strip().split()))
def toStr(n,base):
   convertString = "0123456789ABCDEF"
   if n < base:
      return convertString[n]
   else:
      return toStr(n//base,base) + convertString[n%base]
with open("boundaries1.txt") as f1:
    for line in f1:
        q_bnds.append([float(x) for x in line.strip().split(",")])
print(q_bnds)
n=6
tuple_list=[]
for i in range(0,n**5):
    g=toStr(i,6)
    if len(g)!=5:
        g="0"*(5-len(g))+g
    j=tuple(int(x) for x in g)
    tuple_list.append(j)
#print(tuple_list)
quantized_train=[]
for row in train:
    tup=tuple()
    for b in q_bnds:
        for i in range(0,4):
            if row[i]<b[i]:
                tup=tup+(i,)
                break
            elif row[i]<b[i+1]:
                tup+=(i+1,)
                break
            elif row[i]<b[i+2]:
                tup+=(i+2,)
                break
    tup+=(row[5],)
    if len(tup)>1:
        quantized_train.append(tup)
pcd=[[],[]]
pd=[]
#print(quantized_train)
for q in quantized_train:
    pd.append(q[:-1])
    if q[-1]==1.0:
        pcd[1].append(q[:-1])
    else:
        pcd[0].append(q[:-1])
counter_pcd1=[]
counter_pcd1.append(Counter(tuple(x) for x in iter(pcd[0])))
counter_pcd1.append(Counter(tuple(x) for x in iter(pcd[1])))
counter_pd=Counter(tuple(x) for x in iter(pd))
g=list(counter_pd.keys())
print(counter_pcd1)
#counter_pcd.remove((0, 0, 0, 0, 0))
#sum0=sum(counter_pcd[0].values())
#sum1=sum(counter_pcd[1].values())
# print(counter_pcd)

economic_gain=[[1,-1],[-2,3]]
print(counter_pcd1)
gain1=0
final_counter=[]
for mul in range(1,5):
    counter_pcd=copy.deepcopy(counter_pcd1)
    sum0 = sum(counter_pcd[0].values())
    sum1 = sum(counter_pcd[1].values())
    k=3333333*mul/6
    print(k)
    for tup in tuple_list:
        l=tup
        vm = 1
        for i in range(0, len(tup)):
            if tup[i] == 0:
                vm = vm * q_bnds[i][tup[i]]
            else:
                vm = vm * (q_bnds[i][tup[i]] - q_bnds[i][tup[i] - 1])
        #print("tuple",tup)
        for c in range(0,2):
            bm=counter_pcd[c][tup]
            sum_vm=vm
            #print("sum_vm bfro",sum_vm)
            #print("bm bfre",bm)
            #count=0
            for i in range(0,5):
                #print(tup)
                if tup[i]!=0 and bm<k:
                    h=list(tup)
                    h[i]=h[i]-1
                    tup=tuple(h)
                    bm=bm+counter_pcd[c][tup]
                    vb=1
                    for i in range(0, len(tup)):
                        if tup[i]==0:
                            vb = vb * q_bnds[i][tup[i]]
                        else:
                            vb=vb * (q_bnds[i][tup[i]]- q_bnds[i][tup[i]-1])
                    sum_vm=sum_vm+vb
                if tup[i]!=5 and bm<k:
                    h = list(tup)
                    h[i] = h[i] + 1
                    tup = tuple(h)
                    bm = bm + counter_pcd[c][tup]
                    vb = 1
                    for i in range(0, len(tup)):
                        if tup[i]==0:
                            vb = vb * q_bnds[i][tup[i]]
                        else:
                            vb=vb * (q_bnds[i][tup[i]]- q_bnds[i][tup[i]-1])
                    sum_vm = sum_vm + vb
                #print(tup)
                #print("count",count)
                #print("after sum",sum_vm)
                #print("bm",bm)
                #count=count+1
                if bm>k:
                    break
                #print(count)
            #print("after sum",sum_vm)
            #print("bm",bm)
            counter_pcd[c][tup]=bm*vm/sum_vm
    print(counter_pcd)
    sum0=sum(counter_pcd[0].values())
    sum1=sum(counter_pcd[1].values())
    # print(counter_pcd)
    for tup in tuple_list:
        if counter_pcd[0][tup]!=0:
            counter_pcd[0][tup] = ((counter_pcd[0][tup] / sum0)) * 0.4 / (
                    ((counter_pcd[0][tup] / sum0)) * 0.4 + ((counter_pcd[1][tup] / sum1)) * 0.6)
        if counter_pcd[1][tup]!=0:
            counter_pcd[1][tup] = ((counter_pcd[1][tup] / sum0)) * 0.4 / (
                    ((counter_pcd[0][tup] / sum0)) * 0.4 + ((counter_pcd[1][tup] / sum1)) * 0.6)
    print(counter_pcd)
    assigned=[]
    gain=0
    ev=[]
    filename1=open("eval.txt")
    for line in filename1:
        tup = tuple()
        row = [float(x) for x in line.strip().split()]
        for b in q_bnds:
            for i in range(0, 4):
                if row[i] < b[i]:
                    tup = tup + (i,)
                    break
                elif row[i] < b[i + 1]:
                    tup += (i + 1,)
                    break
                elif row[i] < b[i + 2]:
                    tup += (i + 2,)
                    break
        tup += (row[5],)
        ev.append(tup)

    for q in ev:
        f0=counter_pcd[0][q[:-1]]*economic_gain[0][0]+counter_pcd[1][q[:-1]]*economic_gain[1][0]
        f1=counter_pcd[0][q[:-1]]*economic_gain[0][1]+counter_pcd[1][q[:-1]]*economic_gain[1][1]
        assigned=1
        if f0>f1:
            assigned=0
        if assigned==0 and q[-1]==1.0:
            gain+=economic_gain[0][1]*counter_pcd[0][q[:-1]]
        elif assigned==0 and q[-1]==0.0:
            gain+=economic_gain[0][0]*counter_pcd[0][q[:-1]]
        elif assigned==1 and q[-1]==1.0:
            gain+=economic_gain[1][1]*counter_pcd[1][q[:-1]]
        elif assigned==1 and q[-1]==0.0:
            gain+=economic_gain[1][0]*counter_pcd[1][q[:-1]]
    print(gain)
    if gain1<gain:
        gain1=gain
        final_counter=copy.deepcopy(counter_pcd)
print(gain1)
test=[]
filename2=open("test.txt")
for line in filename2:
    tup = tuple()
    row = [float(x) for x in line.strip().split()]
    for b in q_bnds:
        for i in range(0, 4):
            if row[i] < b[i]:
                tup = tup + (i,)
                break
            elif row[i] < b[i + 1]:
                tup += (i + 1,)
                break
            elif row[i] < b[i + 2]:
                tup += (i + 2,)
                break
    tup += (row[5],)
    test.append(tup)
gain=0
tp=0
fp=0
tn=0
fn=0
for q in test:
    f0 = final_counter[0][q[:-1]] * economic_gain[0][0] + final_counter[1][q[:-1]] * economic_gain[1][0]
    f1 = final_counter[0][q[:-1]] * economic_gain[0][1] + final_counter[1][q[:-1]] * economic_gain[1][1]
    assigned = 1
    if f0 > f1:
        assigned = 0
    if assigned == 0 and q[-1] == 1.0:
        gain += economic_gain[0][1] * final_counter[0][q[:-1]]
        fp+=1
    elif assigned == 0 and q[-1] == 0.0:
        gain += economic_gain[0][0] * final_counter[0][q[:-1]]
        tn+=1
    elif assigned == 1 and q[-1] == 1.0:
        gain += economic_gain[1][1] * final_counter[1][q[:-1]]
        tp+=1
    elif assigned == 1 and q[-1] == 0.0:
        gain += economic_gain[1][0] * final_counter[1][q[:-1]]
        fn+=1
print(gain)
print("false positive:",fp)
print("false negative:",fn)
print("true positive:",tp)
print("true negative:",tn)