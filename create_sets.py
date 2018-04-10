from __future__ import division
from collections import Counter

import math
l=[]
entropy_list=[]
eval=open("eval.txt","w")
train=open("train.txt","w")
test=open("test.txt","w")
with open("pr_data.txt") as filename:
    count=0
    for line in filename:
        if count<3333334:
            train.write(line)
        elif count>3333334 and count<6666667:
            eval.write(line)
        else:
            test.write(line)
        count+=1
