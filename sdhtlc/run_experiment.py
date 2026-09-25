from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import pandas as pd
from .compliance.credentials import generate_credentials
from .compliance.policy import Policy
from .simulation.workload import generate_workload
from .simulation.engine import run_swap
from .evaluation.metrics import summarize,rates
from .evaluation.tables import write_tables
from .evaluation.figures import generate_figures
from .arbitration.committee import collusion_probability

METHODS=["B0","B1","B2","B3","B4","B5"]

def cfg_hash(x): return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()

def run_condition(exp,seeds,n):
 rows=[]
 for seed in range(seeds):
  creds=generate_credentials(50000,seed); policy=Policy()
  for row in generate_workload(n,seed):
   c=creds[row["credential"]%len(creds)]
   if exp=="E3":
    configs=[3,5,7,9]
   elif exp=="E4":
    configs=[5]
   else: configs=[5]
   for k in configs:
    methods=METHODS if exp in ("E1","E2") else (["B1","B2","B4"] if exp=="E2" else ["B4"])
    if exp=="E6": methods=["B0","B1","B3","B4"]
    for method in methods:
     for fault in ([0,.1,.2,.3,.4,.5] if exp=="E2" else [0.0]):
      for byz in ([0,.1,.2,.3,.4] if exp=="E4" else [0.0]):
       r=run_swap(method,row,c,policy,seed,committee_size=k,fault_rate=fault,byzantine=byz)
       r.update({"experiment":exp,"seed":seed,"fault_rate":fault,"byzantine_fraction":byz,"committee_size":k,
                 "configuration_hash":cfg_hash({"exp":exp,"k":k,"fault":fault,"byz":byz})})
       rows.append(r)
 return pd.DataFrame(rows)

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--experiment",choices=["smoke","E1","E2","E3","E4","E5","E6","all"],default="smoke")
 ap.add_argument("--seeds",type=int,default=20); ap.add_argument("--swaps-per-seed",type=int,default=1000)
 args=ap.parse_args()
 Path("results/raw").mkdir(parents=True,exist_ok=True)
 exps=["E1","E2","E3","E4","E5","E6"] if args.experiment=="all" else (["E1"] if args.experiment=="smoke" else [args.experiment])
 frames=[]
 for exp in exps:
  frames.append(run_condition(exp,1 if args.experiment=="smoke" else args.seeds,25 if args.experiment=="smoke" else args.swaps_per_seed))
 df=pd.concat(frames,ignore_index=True); df.to_csv("results/raw/results.csv",index=False)
 summarize(df).to_csv("results/statistics_summary.csv",index=False); write_tables(df); generate_figures(df)
 print(json.dumps({"rows":len(df),"rates":rates(df),"collusion_theory":{str(k):collusion_probability(k,.2) for k in [3,5,7,9]}},indent=2))

if __name__=="__main__": main()
