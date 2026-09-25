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

METHODS=["B0","B1","B2","B3","B4","B5"]

def config_hash(cfg): return hashlib.sha256(json.dumps(cfg,sort_keys=True).encode()).hexdigest()

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--experiment",choices=["smoke","E1","E2","E3","E4","E5","E6","all"],default="smoke"); ap.add_argument("--seeds",type=int,default=20); ap.add_argument("--swaps-per-seed",type=int,default=1000); args=ap.parse_args()
 seeds=1 if args.experiment=="smoke" else args.seeds; n=25 if args.experiment=="smoke" else args.swaps_per_seed
 Path("results/raw").mkdir(parents=True,exist_ok=True); rows=[]
 methods=METHODS if args.experiment in ("E1","E2","all") else ["B4"]
 for seed in range(seeds):
  creds=generate_credentials(50000 if n>25 else max(100,n),seed); policy=Policy()
  for row in generate_workload(n,seed):
   c=creds[row["credential"]%len(creds)]
   for method in methods:
    fault=0.2 if args.experiment=="E2" else 0.0; byz=.2 if args.experiment=="E4" else 0.0
    r=run_swap(method,row,c,policy,seed,committee_size=5,fault_rate=fault,byzantine=byz); r.update({"experiment":args.experiment,"seed":seed,"fault_rate":fault,"configuration_hash":config_hash(vars(args))}); rows.append(r)
 df=pd.DataFrame(rows); df.to_csv("results/raw/results.csv",index=False); summarize(df).to_csv("results/statistics_summary.csv",index=False); write_tables(df); generate_figures(df); print(rates(df)); print("rows:",len(df))

if __name__=="__main__": main()
