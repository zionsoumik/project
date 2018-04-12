from __future__ import division
from collections import Counter
import csv
import copy
import math
l=[]
entropy_list=[]
filename1=open("eval.txt")
filename=open("train.txt")
for line in filename:
    l.append(tuple(float(x) for x in line.strip().split()))
mydict=Counter(x[:-1] for x in l)
g=list(mydict.keys())
boundaries=[]
for num1 in range(0,len(g[1])):
    h=[]
    for x in g:
        if len(x)==5:
            h.append(x[num1])
    h=sorted(h)
    b=[]
    count=math.floor(len(l)/6)
    for i in range(0,5):
        b.append(h[count])
        count += math.floor(len(l) / 6)
    b.append(1)
    boundaries.append(b)
#print(boundaries)
#print(len(h))
#print(len(l))
quantized_data=[]
for row in l:
    tup=tuple()
    for b in boundaries:
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
    quantized_data.append(tup)
# with open("out.txt","w", newline='') as f:
#     wr = csv.writer(f)
#     wr.writerows(quantized_data)
pcd=[[],[]]
pd=[]
for q in quantized_data:
    pd.append(q[:-1])
    if q[-1]==1.0:
        pcd[1].append(q[:-1])
    else:
        pcd[0].append(q[:-1])
counter_pcd=[]
counter_pcd.append(Counter(tuple(x) for x in iter(pcd[0])))
counter_pcd.append(Counter(tuple(x) for x in iter(pcd[1])))
counter_pd=Counter(tuple(x) for x in iter(pd))
g=list(counter_pd.keys())
# print(counter_pd)
sum0=sum(counter_pcd[0].values())
sum1=sum(counter_pcd[1].values())
# print(counter_pcd)
for i in range(0, len(g)):
    #print(g[i])
    if g[i] in list(counter_pcd[0].keys()):
        counter_pcd[0][g[i]]=((counter_pcd[0][g[i]]/sum0))*0.4/(((counter_pcd[0][g[i]]/sum0))*0.4+((counter_pcd[1][g[i]]/sum1))*0.6)
    if g[i] in list(counter_pcd[1].keys()):
        counter_pcd[1][g[i]] = ((counter_pcd[1][g[i]] / sum1)) * 0.6 / (((counter_pcd[0][g[i]] / sum0)) * 0.4 + ((counter_pcd[1][g[i]] / sum1)) * 0.6)
economic_gain=[[1,-1],[-2,3]]
#print("counter pcd:",counter_pcd)
assigned=[]
gain=0
ev=[]
filename1=open("eval.txt")
for line in filename1:
    tup = tuple()
    row = [float(x) for x in line.strip().split()]
    for b in boundaries:
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
        gain+=economic_gain[0][1]
    elif assigned==0 and q[-1]==0.0:
        gain+=economic_gain[0][0]
    elif assigned==1 and q[-1]==1.0:
        gain+=economic_gain[1][1]
    elif assigned==1 and q[-1]==0.0:
        gain+=economic_gain[1][0]
#print(gain)
for c1 in range(0,len(boundaries)):
    for c2 in range(0,5):
        new_boundaries=copy.deepcopy(boundaries)
        if c2==0:
            bt1=0
        else:
            bt1=boundaries[c1][c2-1]
        bt2=boundaries[c1][c2+1]
        left=bt1+3*(boundaries[c1][c2]-bt1)/4
        right=bt2-3*(bt2-boundaries[c1][c2])/4
        b0=boundaries[c1][c2]
        step=(left-right)/10
        for num2 in range(0,10):
            boundaries_list=[]
            gain_list=[]

            #print("old boundaries",boundaries)
            b1 = left + (num2) * step
            new_boundaries[c1][c2]=b1
            #print("new_bounds",new_boundaries)
            new_q_data=copy.deepcopy(quantized_data)
            #count=math.floor(len(l)/7)
            for i in range (0,len(l)):
                clas=0
                if l[i][c2]<b1:
                    clas=0
                    break
                elif l[i][c2]<new_boundaries[c1][c2+1]:
                    clas=1
                    break
                new_q_data[i]=list(new_q_data[i])
                new_q_data[i][c2]=clas
                new_q_data[i]=tuple(new_q_data[i])
            #print("len of new_data",len(new_q_data))
            # with open("out.txt","w", newline='') as f:
            #     wr = csv.writer(f)
            #     wr.writerows(new_q_data)
            pcd=[[],[]]
            pd=[]
            for q in new_q_data:
                pd.append(q[:-1])
                if q[-1]==1.0:
                    pcd[1].append(q[:-1])
                else:
                    pcd[0].append(q[:-1])
            counter_pcd=[]
            counter_pcd.append(Counter(tuple(x) for x in iter(pcd[0])))
            counter_pcd.append(Counter(tuple(x) for x in iter(pcd[1])))
            counter_pd=Counter(tuple(x) for x in iter(pd))
            g=list(counter_pd.keys())
            sum0 = sum(counter_pcd[0].values())
            sum1 = sum(counter_pcd[1].values())
            #print(counter_pcd)
            #print(counter_pd)
            for i in range(0, len(g)):
                # print(g[i])
                if g[i] in list(counter_pcd[0].keys()):
                    counter_pcd[0][g[i]] = ((counter_pcd[0][g[i]] / sum0)) * 0.4 / (((counter_pcd[0][g[i]] / sum0)) * 0.4 + ((counter_pcd[1][g[i]] / sum1)) * 0.6)
                if g[i] in list(counter_pcd[1].keys()):
                    counter_pcd[1][g[i]] = ((counter_pcd[1][g[i]] / sum1)) * 0.6 / (((counter_pcd[0][g[i]] / sum0)) * 0.4 + ((counter_pcd[1][g[i]] / sum1)) * 0.6)
            economic_gain = [[1, -1], [-2, 3]]
            #print(counter_pcd)

            assigned=[]
            gain1=0
            ev1=[]
            filename1.close()
            filename1=open("eval.txt")
            for line in filename1:
                tup = tuple()
                row = [float(x) for x in line.strip().split()]
                for b in new_boundaries:
                    for i in range(0, 5):
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
                ev1.append(tup)
            new_counter_pd = Counter(x for x in ev1)
            g = list(new_counter_pd.keys())
            new_sum = sum(new_counter_pd.values())
            # new_sum1 = sum(new_counter_pcd[1].values())

            # print(counter_pd)
            for i in range(0, len(g)):
                # print(g[i])
                new_counter_pd[g[i]] = new_counter_pd[g[i]] / new_sum
            economic_gain = [[1, -1], [-2, 3]]
            #print("new_counter:", new_counter_pd)
            # new_sum0 = sum(new_counter_pcd[0].values())
            # new_sum1 = sum(new_counter_pcd[1].values())
            # print("new_sum",new_sum1,new_sum0)
            gain = 0
            for q in new_counter_pd.keys():
                #print(q[:-1])
                f0 = counter_pcd[0][q[:-1]] * economic_gain[0][0] + counter_pcd[1][q[:-1]] * economic_gain[1][0]
                f1 = counter_pcd[0][q[:-1]] * economic_gain[0][1] + counter_pcd[1][q[:-1]] * economic_gain[1][1]
                assigned = 1
                #print("f0", f0)
                #print("f1", f1)
                if f0 > f1:
                    assigned = 0
                #print(q[-1])
                if assigned == 0 and q[-1] == 1.0:
                    gain += economic_gain[0][1] * new_counter_pd[q]
                elif assigned == 0 and q[-1] == 0.0:
                    gain += economic_gain[0][0] * new_counter_pd[q]
                elif assigned == 1 and q[-1] == 1.0:
                    gain += economic_gain[1][1] * new_counter_pd[q]
                elif assigned == 1 and q[-1] == 0.0:
                    gain += economic_gain[1][0] * new_counter_pd[q]
            if gain>gain1:
                #print("gain1",gain)
                gain1=gain
                boundaries[c1][c2]=b1
print("gain:",gain1)
print(boundaries)
with open("boundaries3.txt","w", newline='') as f:
    wr = csv.writer(f)
    wr.writerows(boundaries)