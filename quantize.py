from __future__ import division
from collections import Counter
import csv
import copy
import math
import random
tp=0
tn=0
l=[]
entropy_list=[]
#filename1=open("eval.txt")
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
    count=int(math.ceil(len(l)/7))
    #print(count)
    for i in range(0,6):
        b.append(h[count])
        if i%2==0:
            count += int(math.floor(len(l) / 7))
        else:
            count += int(math.ceil(len(l) / 7))
    b.append(1)
    boundaries.append(b)
print(boundaries)
#print(len(h))
#print(len(l))
random.seed(1237)
quantized_data=[]
for row in l:
    tup=tuple()
    #print(row)
    for i in range(0, 5):
        for j in range(0,len(boundaries[i])):
            if row[i]<boundaries[i][j]:
                #print(row[i])
                #print(boundaries[i][j])
                tup=tup+(j,)
                break
            # elif row[i]<b[i+1]:
            #     tup+=(i+1,)
            #     break
            # elif row[i]<b[i+2]:
            #     tup+=(i+2,)
            #     break
    tup+=(row[5],)
    #print(tup)
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
#print(counter_pcd)
for i in range(0, len(g)):
    #print(g[i])
    l0=0
    l1=0
    if g[i] in list(counter_pcd[0].keys()):
        l0 = ((counter_pcd[0][g[i]]) / sum0) * 0.4 / (
                ((counter_pcd[0][g[i]]) / sum0) * 0.4 + ((counter_pcd[1][g[i]]) / sum1) * 0.6)
    if g[i] in list(counter_pcd[1].keys()):
        l1 = ((counter_pcd[1][g[i]]) / sum1) * 0.6 / (
                ((counter_pcd[0][g[i]]) / sum0) * 0.4 + ((counter_pcd[1][g[i]]) / sum1) * 0.6)
    counter_pcd[0][g[i]] = l0
    counter_pcd[1][g[i]] = l1
economic_gain=[[1,-1],[-2,3]]
#print("counter pcd:",counter_pcd)
assigned=[]
gain=0
#ev=[]
# filename1=open("eval.txt")
# for line in filename1:
#     tup = tuple()
#     row = [float(x) for x in line.strip().split()]
#     for b in boundaries:
#         for i in range(0, 5):
#             if row[i] < b[i]:
#                 tup = tup + (i,)
#                 break
#             elif row[i] < b[i + 1]:
#                 tup += (i + 1,)
#                 break
#             elif row[i] < b[i + 2]:
#                 tup += (i + 2,)
#                 break
#     tup += (row[5],)
#     ev.append(tup)

# for q in ev:
#     f0=counter_pcd[0][q[:-1]]*economic_gain[0][0]+counter_pcd[1][q[:-1]]*economic_gain[1][0]
#     f1=counter_pcd[0][q[:-1]]*economic_gain[0][1]+counter_pcd[1][q[:-1]]*economic_gain[1][1]
#     assigned=1
#     if f0>f1:
#         assigned=0
#     if assigned==0 and q[-1]==1.0:
#         gain+=economic_gain[0][1]
#     elif assigned==0 and q[-1]==0.0:
#         gain+=economic_gain[0][0]
#     elif assigned==1 and q[-1]==1.0:
#         gain+=economic_gain[1][1]
#     elif assigned==1 and q[-1]==0.0:
#         gain+=economic_gain[1][0]
#print(gain)
#print(boundaries)
gain1=0
count=0
while count<2000:
    c1=random.randint(0,len(boundaries)-1)
    c2=random.randint(0,len(boundaries[num1])-2)
    new_boundaries = copy.deepcopy(boundaries)
    if c2 == 0:
        bt1 = 0
    else:
        bt1 = boundaries[c1][c2 - 1]
    bt2 = boundaries[c1][c2 + 1]
    #left = bt1 + 3 * (boundaries[c1][c2] - bt1) / 4
    #right = bt2 - 3 * (bt2 - boundaries[c1][c2]) / 4
    b1=random.uniform(bt1,bt2)
    new_boundaries[c1][c2] = b1
    #print(new_boundaries)

    new_q_data = []
    # count=math.floor(len(l)/7)
    for row in l:
        tup = tuple()
        for i in range(0, 5):
            for j in range(0, len(new_boundaries[i])):
                if row[i] < new_boundaries[i][j]:
                    #print(row[i])
                    #print(new_boundaries[i][j])
                    tup = tup + (j,)
                    break
                # elif row[i]<b[i+1]:
                #     tup+=(i+1,)
                #     break
                # elif row[i]<b[i+2]:
                #     tup+=(i+2,)
                #     break
        tup += (row[5],)
        new_q_data.append(tup)
    ##print(new_q_data)
    pcd = [[], []]
    pd = []
    for q in new_q_data:
        pd.append(q[:-1])
        if q[-1] == 1.0:
            pcd[1].append(q[:-1])
        else:
            pcd[0].append(q[:-1])
    counter_pcd = []
    counter_pcd.append(Counter(tuple(x) for x in iter(pcd[0])))
    counter_pcd.append(Counter(tuple(x) for x in iter(pcd[1])))
    counter_pd = Counter(tuple(x) for x in iter(pd))
    g = list(counter_pd.keys())
    sum0 = sum(counter_pcd[0].values())
    sum1 = sum(counter_pcd[1].values())
    #print(counter_pcd)
    #print(counter_pd)
    for i in range(0, len(g)):
        #print(g[i])
        l0 = 0
        l1 = 0
        if g[i] in list(counter_pcd[0].keys()):
            l0 = ((counter_pcd[0][g[i]]) / sum0) * 0.4 / (
                    ((counter_pcd[0][g[i]]) / sum0) * 0.4 + ((counter_pcd[1][g[i]]) / sum1) * 0.6)
        if g[i] in list(counter_pcd[1].keys()):
            l1 = ((counter_pcd[1][g[i]]) / sum1) * 0.6 / (
                    ((counter_pcd[0][g[i]]) / sum0) * 0.4 + ((counter_pcd[1][g[i]]) / sum1) * 0.6)
        counter_pcd[0][g[i]] = l0
        counter_pcd[1][g[i]] = l1
    economic_gain = [[1, -1], [-2, 3]]
    # print(counter_pcd)

    assigned = []

    ev1 = []
    # filename1.close()
    with open("eval.txt") as filename1:
        for line in filename1:
            tup = tuple()
            row = [float(x) for x in line.strip().split()]
            for i in range(0, 5):
                for j in range(0, len(new_boundaries[i])):
                    if row[i] < new_boundaries[i][j]:
                        # print(row[i])
                        # print(boundaries[i][j])
                        tup = tup + (j,)
                        break
                    # elif row[i]<b[i+1]:
                    #     tup+=(i+1,)
                    #     break
                    # elif row[i]<b[i+2]:
                    #     tup+=(i+2,)
                    #     break
            tup += (row[5],)
            # print(tup)
            ev1.append(tup)
    # new_counter_pd = Counter(x for x in ev1)
    # g = list(new_counter_pd.keys())
    # new_sum = sum(new_counter_pd.values())
    # new_sum1 = sum(new_counter_pcd[1].values())

    # print(counter_pd)
    # for i in range(0, len(g)):
    #     # print(g[i])
    #     new_counter_pd[g[i]] = new_counter_pd[g[i]] / new_sum
    economic_gain = [[1, -1], [-2, 3]]
    # print("new_counter:", new_counter_pd)
    # new_sum0 = sum(new_counter_pcd[0].values())
    # new_sum1 = sum(new_counter_pcd[1].values())
    # print("new_sum",new_sum1,new_sum0)
    gain = 0
    tp1 = 0
    tn1 = 0
    for q in ev1:
        # print(q[:-1])
        f0 = counter_pcd[0][q[:-1]] * economic_gain[0][0] + counter_pcd[1][q[:-1]] * economic_gain[0][1]
        f1 = counter_pcd[0][q[:-1]] * economic_gain[1][0] + counter_pcd[1][q[:-1]] * economic_gain[1][1]
        assigned = 1
        # print("f0", f0)
        # print("f1", f1)
        if f0 > f1:
            assigned = 0
        # print(q[-1])
        if assigned == 0 and q[-1] == 1.0:
            gain += economic_gain[0][1]
        elif assigned == 0 and q[-1] == 0.0:
            gain += economic_gain[0][0]
            tn1 += 1
        elif assigned == 1 and q[-1] == 1.0:
            gain += economic_gain[1][1]
            tp1 += 1
        elif assigned == 1 and q[-1] == 0.0:
            gain += economic_gain[1][0]
    # print(new_boundaries)
    if gain1 < gain:
        #print("gain1", gain / len(ev1))
        gain1 = gain
        tp = tp1
        tn = tn1
        #print("accuracy", (tn1 + tp1) / len(ev1))
        boundaries[c1][c2] = b1
        #print(boundaries)
        count = 0
    else:
        count += 1
#gain=gain1
for c1 in range(0,len(boundaries)):
    for c2 in range(0,6):
        new_boundaries=copy.deepcopy(boundaries)
        if c2==0:
            bt1=0
        else:
            bt1=boundaries[c1][c2-1]
        bt2=boundaries[c1][c2+1]
        left=bt1+3*(boundaries[c1][c2]-bt1)/4
        right=bt2-3*(bt2-boundaries[c1][c2])/4
        b0=boundaries[c1][c2]
        step=(right-left)/10
        #print(left,right)
        for num2 in range(0,10):
            boundaries_list=[]
            gain_list=[]

            #print("old boundaries",boundaries)
            b1 = left + (num2) * step
            new_boundaries[c1][c2]=b1
            #print("new_bounds",new_boundaries)
            new_q_data=[]
            #count=math.floor(len(l)/7)
            for row in l:
                tup = tuple()
                for i in range(0, 5):
                    for j in range(0, len(new_boundaries[i])):
                        if row[i] < new_boundaries[i][j]:
                            # print(row[i])
                            # print(boundaries[i][j])
                            tup = tup + (j,)
                            break
                        # elif row[i]<b[i+1]:
                        #     tup+=(i+1,)
                        #     break
                        # elif row[i]<b[i+2]:
                        #     tup+=(i+2,)
                        #     break
                tup += (row[5],)
                new_q_data.append(tup)
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
                l0 = 0
                l1 = 0
                if g[i] in list(counter_pcd[0].keys()):
                    l0 = ((counter_pcd[0][g[i]])/sum0) * 0.4 / (
                            ((counter_pcd[0][g[i]])/sum0) * 0.4 + ((counter_pcd[1][g[i]])/sum1)* 0.6)
                if g[i] in list(counter_pcd[1].keys()):
                    l1 = ((counter_pcd[1][g[i]])/sum1) * 0.6 / (
                            ((counter_pcd[0][g[i]])/sum0) * 0.4 + ((counter_pcd[1][g[i]])/sum1) * 0.6)
                counter_pcd[0][g[i]] = l0
                counter_pcd[1][g[i]] = l1
            economic_gain = [[1, -1], [-2, 3]]
            #print(counter_pcd)

            assigned=[]

            ev1=[]
            #filename1.close()
            with open("eval.txt") as filename1:
                for line in filename1:
                    tup = tuple()
                    row = [float(x) for x in line.strip().split()]
                    for i in range(0, 5):
                        for j in range(0, len(new_boundaries[i])):
                            if row[i] < new_boundaries[i][j]:
                                # print(row[i])
                                # print(boundaries[i][j])
                                tup = tup + (j,)
                                break
                            # elif row[i]<b[i+1]:
                            #     tup+=(i+1,)
                            #     break
                            # elif row[i]<b[i+2]:
                            #     tup+=(i+2,)
                            #     break
                    tup += (row[5],)
                    #print(tup)
                    ev1.append(tup)
            #new_counter_pd = Counter(x for x in ev1)
            #g = list(new_counter_pd.keys())
            # new_sum = sum(new_counter_pd.values())
            # new_sum1 = sum(new_counter_pcd[1].values())

            # print(counter_pd)
            # for i in range(0, len(g)):
            #     # print(g[i])
            #     new_counter_pd[g[i]] = new_counter_pd[g[i]] / new_sum
            economic_gain = [[1, -1], [-2, 3]]
            #print("new_counter:", new_counter_pd)
            # new_sum0 = sum(new_counter_pcd[0].values())
            # new_sum1 = sum(new_counter_pcd[1].values())
            # print("new_sum",new_sum1,new_sum0)
            gain = 0
            tp1=0
            tn1=0
            for q in ev1:
                #print(q[:-1])
                f0 = counter_pcd[0][q[:-1]] * economic_gain[0][0] + counter_pcd[1][q[:-1]] * economic_gain[0][1]
                f1 = counter_pcd[0][q[:-1]] * economic_gain[1][0] + counter_pcd[1][q[:-1]] * economic_gain[1][1]
                assigned = 1
                #print("f0", f0)
                #print("f1", f1)
                if f0 > f1:
                    assigned = 0
                #print(q[-1])
                if assigned == 0 and q[-1] == 1.0:
                    gain += economic_gain[0][1]
                elif assigned == 0 and q[-1] == 0.0:
                    gain += economic_gain[0][0]
                    tn1+=1
                elif assigned == 1 and q[-1] == 1.0:
                    gain += economic_gain[1][1]
                    tp1+=1
                elif assigned == 1 and q[-1] == 0.0:
                    gain += economic_gain[1][0]
            #print(new_boundaries)
            if gain1<gain:
                #print("gain1",gain/len(ev1))
                gain1=gain
                tp=tp1
                tn=tn1
                #print("accuracy", (tn1 + tp1) / len(ev1))
                boundaries[c1][c2]=b1
                #print(boundaries)
            # else:
            #     print("gain",gain/len(ev1))
            #     print("accuracy", (tn1 + tp1) / len(ev1))
print("gain:",gain1/len(ev1))
print(boundaries)
print("accuracy",(tn+tp)/len(ev1))
with open("boundaries5.txt","w", newline='') as f:
    wr = csv.writer(f)
    wr.writerows(boundaries)