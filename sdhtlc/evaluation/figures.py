from pathlib import Path
import matplotlib.pyplot as plt

def generate_figures(df,out="results/figures"):
 Path(out).mkdir(parents=True,exist_ok=True)
 for name,y,x in [("fault_liveness","completed","fault_rate"),("arb_latency","arb_ms","committee_size"),("gas","gas","method"),("privacy","disclosure_count","method")]:
  if x not in df or y not in df: continue
  g=df.groupby(x)[y].mean()
  fig,ax=plt.subplots(); g.plot(kind="line" if len(g)>1 else "bar",ax=ax); ax.set_ylabel(y); ax.set_xlabel(x); fig.tight_layout(); fig.savefig(Path(out)/(name+".png")); plt.close(fig)
