import numpy as np
from scipy import stats

def bootstrap_ci(x,b=2000,seed=42):
 x=np.asarray(x,float); rng=np.random.default_rng(seed)
 means=np.array([rng.choice(x,len(x),replace=True).mean() for _ in range(b)])
 return float(np.quantile(means,.025)),float(np.quantile(means,.975))

def paired_permutation(a,b,reps=5000,seed=42):
 a=np.asarray(a,float); b=np.asarray(b,float); d=a-b; rng=np.random.default_rng(seed); obs=abs(d.mean())
 vals=np.array([abs((d*rng.choice([-1,1],len(d))).mean()) for _ in range(reps)])
 return float((np.sum(vals>=obs)+1)/(reps+1))

def effect_size(a,b):
 d=np.asarray(a,float)-np.asarray(b,float); return float(d.mean()/(d.std(ddof=1) or 1.0))

def benjamini_hochberg(p):
 p=np.asarray(p,float); order=np.argsort(p); q=np.empty(len(p)); running=1.
 for rank,i in reversed(list(enumerate(order,1))): running=min(running,p[i]*len(p)/rank); q[i]=running
 return q

def mcnemar(a,b):
 a=np.asarray(a).astype(bool); b=np.asarray(b).astype(bool)
 b01=int(np.sum((a==False)&(b==True))); b10=int(np.sum((a==True)&(b==False)))
 n=b01+b10
 if n==0: return {"b01":b01,"b10":b10,"p_value":1.0}
 p=2*min(stats.binom.cdf(min(b01,b10),n,.5),1-stats.binom.cdf(min(b01,b10)-1,n,.5))
 return {"b01":b01,"b10":b10,"p_value":min(1.0,float(p))}

def compare(a,b):
 d=np.asarray(a)-np.asarray(b); lo,hi=bootstrap_ci(d)
 return {"p_value":paired_permutation(a,b),"ci_low":lo,"ci_high":hi,"effect_size":effect_size(a,b)}
