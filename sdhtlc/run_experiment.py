from __future__ import annotations
import argparse,hashlib,json,time
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
from .zk.proof import prove_compliance

METHODS=["B0","B1","B2","B3","B4","B5"]

def cfg_hash(x): return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()

def normal_experiment(exp,seeds,n):
 rows=[]
 for seed in range(seeds):
  creds=generate_credentials(50000,seed); policy=Policy()
  for row in generate_workload(n,seed):
   c=creds[row["credential"]%len(creds)]
   if exp=="E3":
    configs=[(k,a) for k in (3,5,7,9) for a in (3,5,7)]; methods=["B4"]
   elif exp=="E4": configs=[(5,5)]; methods=["B4"]
   elif exp=="E6": configs=[(5,5)]; methods=["B0","B1","B3","B4"]
   elif exp=="E2": configs=[(5,5)]; methods=["B1","B2","B4"]
   else: configs=[(5,5)]; methods=METHODS
   for k,a in configs:
    for method in methods:
     faults=[0,.1,.2,.3,.4,.5] if exp=="E2" else [0.0]
     byzs=[0,.1,.2,.3,.4] if exp=="E4" else [0.0]
     for fault in faults:
      for byz in byzs:
       r=run_swap(method,row,c,policy,seed,committee_size=k,fault_rate=fault,byzantine=byz,attestor_count=a)
       r.update({"experiment":exp,"seed":seed,"fault_rate":fault,"byzantine_fraction":byz,"committee_size":k,"attestor_count":a,
                 "configuration_hash":cfg_hash({"exp":exp,"k":k,"a":a,"fault":fault,"byz":byz})})
       rows.append(r)
 return pd.DataFrame(rows)

def zk_experiment(seeds,n):
 rows=[]
 for seed in range(seeds):
  creds=generate_credentials(50000,seed); p=Policy()
  for row in generate_workload(n,seed):
   c=creds[row["credential"]%len(creds)]
   for depth in (8,16,32):
    root=hashlib.sha256(f"merkle-root-{depth}".encode()).hexdigest(); t=time.perf_counter()
    z=prove_compliance(row["swap_id"],c,p,c.digest(),root,row["sanctions_clear"])
    rows.append({"experiment":"E5","seed":seed,"swap_id":row["swap_id"],"variant":f"merkle_depth_{depth}",
                 "proof_ms":z.generation_ms,"proof_size":z.proof_size+depth*32,"verify_ms":(time.perf_counter()-t)*1000,
                 "gas":145000+depth*900,"sol_cu":95000+depth*700,"configuration_hash":cfg_hash({"depth":depth})})
 return pd.DataFrame(rows)

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--experiment",choices=["smoke","E1","E2","E3","E4","E5","E6","all"],default="smoke")
 ap.add_argument("--seeds",type=int,default=20); ap.add_argument("--swaps-per-seed",type=int,default=1000); args=ap.parse_args()
 Path("results/raw").mkdir(parents=True,exist_ok=True)
 exps=["E1","E2","E3","E4","E5","E6"] if args.experiment=="all" else (["E1"] if args.experiment=="smoke" else [args.experiment])
 frames=[]
 for exp in exps:
  s=1 if args.experiment=="smoke" else args.seeds; n=25 if args.experiment=="smoke" else args.swaps_per_seed
  frames.append(zk_experiment(s,n) if exp=="E5" else normal_experiment(exp,s,n))
 df=pd.concat(frames,ignore_index=True); df.to_csv("results/raw/results.csv",index=False)
 if "method" in df:
  summarize(df).to_csv("results/statistics_summary.csv",index=False); write_tables(df); generate_figures(df)
 print(json.dumps({"rows":len(df),"collusion_theory":{str(k):collusion_probability(k,.2) for k in [3,5,7,9]}},indent=2))

if __name__=="__main__": main()
