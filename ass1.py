import pandas as pd
import math
from collections import Counter
df1=pd.read_csv("pr_data2.csv")
hdlist=list(df1.columns.values)
limitlist=[]
entropy_list=[]
prob_list=[]
for hdrs in hdlist:
    k=df1[hdrs]
    l=[]
    for k1 in k:
        l.append(k1)
    l=sorted(l)
    limits=[l[4999],l[9999],l[14999],l[19999],l[24999],l[29999],l[34999],l[39999],l[44999],l[49999]]
    limitlist.append(limits)
    entropy_list.append(-math.log(1/10,2)-1/(2*50000*math.log(2)))
    p_list=[]
    for l in limits:
        p_list.append(1/10)
    prob_list.append(p_list)
sum=0
#print(df1)
#print(entropy_list)
#print(limitlist)
s=pd.DataFrame()
prob_d=[]
prob_c_d=[[],[]]
for j in range(0,50000):
    d={}
    p_d=[]
    #p_c_d=[[],[]]
    for r in range(0,len(hdlist)-1):
            for k in range(0,10):
                #print("limits:",limitlist[r][k],k)
                #print("df1:",df1[hdlist[r]][j])

                if df1[hdlist[r]][j]<limitlist[r][k]:
                    #print("yes")
                    p_d.append(k)
                    #p_c_d.append(k)
                    d[hdlist[r]]=k
                    #print("d:", d)
                    break

    d['V6']=df1['V6'][j]
    #p_c_d.append(df1['V6'][j])
    s1 = pd.DataFrame(d,index=[0])
    prob_d.append(p_d)
    prob_c_d[df1['V6'][j]].append(p_d)
    s=s.append(s1)
    #print(s)
#print(s)
expected_gain=0
print(prob_c_d)
counter_pcd=[]
counter_pcd.append(Counter(tuple(x) for x in iter(prob_c_d[0])))
counter_pcd.append(Counter(tuple(x) for x in iter(prob_c_d[1])))


f1=Counter(tuple(x) for x in iter(prob_d))
for key in f1.keys():
    if key in counter_pcd[0].keys():
        counter_pcd[0][key]=counter_pcd[0][key]/f1[key]
    if key in counter_pcd[1].keys():
        counter_pcd[1][key] = counter_pcd[1][key] / f1[key]


print(counter_pcd)
eval=pd.read_csv("eval.csv")
hdlist=list(eval.columns.values)
gain=0
ev=[]
economic_gain=[]
for q in ev:
    f0 = counter_pcd[0][q[:-1]] * economic_gain[0][0] + counter_pcd[1][q[:-1]] * economic_gain[1][0]
    f1 = counter_pcd[0][q[:-1]] * economic_gain[0][1] + counter_pcd[1][q[:-1]] * economic_gain[1][1]
    assigned = 1
    if f0 > f1:
        assigned = 0
    if assigned == 0 and q[-1] == 1.0:
        gain += economic_gain[0][1] * counter_pcd[0][q[:-1]]
    elif assigned == 0 and q[-1] == 0.0:
        gain += economic_gain[0][0] * counter_pcd[0][q[:-1]]
    elif assigned == 1 and q[-1] == 1.0:
        gain += economic_gain[1][1] * counter_pcd[1][q[:-1]]
    elif assigned == 1 and q[-1] == 0.0:
        gain += economic_gain[1][0] * counter_pcd[1][q[:-1]]
#print(gain)
print(gain)
#print(len(f1))