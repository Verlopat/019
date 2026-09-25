import pandas as pd
from .statistics import compare

def paired_method_comparison(df,method_a,method_b,metric):
 a=df[df.method==method_a].sort_values("swap_id")[metric].to_numpy(); b=df[df.method==method_b].sort_values("swap_id")[metric].to_numpy()
 n=min(len(a),len(b)); return compare(a[:n],b[:n])
