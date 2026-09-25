import numpy as np
import pandas as pd

def summarize(df):
 cols=["atomicity_violation","unauthorized_release","completed","refunded","proof_ms","arb_ms","gas","sol_cu","disclosure_count"]
 return pd.DataFrame([{"metric":c,"mean":df[c].mean(),"median":df[c].median(),"std":df[c].std(ddof=1),"p95":df[c].quantile(.95),"p99":df[c].quantile(.99)} for c in cols if c in df])

def rates(df):
 n=len(df); return {"AVI":df.atomicity_violation.mean(),"USR":df.unauthorized_release.mean(),"SCR":df.completed.mean(),"refund_rate":df.refunded.mean()}
