import pandas as pd
import numpy as np

h=pd.read_csv("pr_data.txt",sep="\t")
train, eval, test=np.split(h.sample(frac=1), [int((1/3)*len(h)), int((2/3)*len(h))])
print(len(train))
print(len(eval))
print(len(test))
train.to_csv("train.txt",sep="\t",index=False,index_label=False)
eval.to_csv("eval.txt",sep="\t",index=False,index_label=False)
test.to_csv("test.txt",sep="\t",index=False,index_label=False)