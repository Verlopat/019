import random

def generate_workload(n,seed):
 r=random.Random(seed)
 for i in range(n):
  yield {"swap_id":f"{seed}-{i:06d}","amount":round(10**r.uniform(1,5),6),"delay":r.uniform(.01,.2),"credential":r.randrange(50000),"sanctions_clear":r.random()>.01}
