import numpy as np
from scipy import stats

def bootstrap_ci(x,b=2000,seed=42):
 x=np.asarray(x,float); rng=np.random.default_rng(seed); means=np.array([rng.choice(x,len(x),replace=True).mean() for _ in range(b)])
 return float(np.quantile(means,.025)),float(np.quantile(means,.975))

def paired_permutation(a,b,reps=5000,seed=42):
 a=np.asarray(a,float); b=np.asarray(b,float); d=a-b; rng=np.random.default_rng(seed); obs=abs(d.mean()); vals=[]
 for _ in range(reps): vals.append(abs((d*rng.choice([-1,1],len(d))).mean()))
 return float((np.sum(np.asarray(vals)>=obs)+1)/(reps+1))

def effect_size(a,b):
 d=np.asarray(a,float)-np.asarray(b,float); return float(d.mean()/(d.std(ddof=1) or 1.0))

def benjamini_hochberg(p):
 p=np.asarray(p,float); order=np.argsort(p); q=np.empty(len(p)); running=1.
 for rank,i in reversed(list(enumerate(order,1))): running=min(running,p[i]*len(p)/rank); q[i]=running
 return q

def compare(a,b):
 p=paired_permutation(a,b); lo,hi=bootstrap_ci(np.asarray(a)-np.asarray(b)); return {"p_value":p,"ci_low":lo,"ci_high":hi,"effect_size":effect_size(a,b)}
