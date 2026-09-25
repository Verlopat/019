import random

def assign_malicious(members,fraction,seed):
 r=random.Random(seed); ids=set(r.sample(range(len(members)),int(len(members)*fraction)))
 for i,m in enumerate(members): m.malicious=i in ids
 return members
