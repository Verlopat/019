from pathlib import Path

def write_tables(df,out="results/processed"):
 Path(out).mkdir(parents=True,exist_ok=True)

 # Normal experiments expose method-level protocol metrics.
 if "method" in df.columns:
  columns={
   "atomicity_violation":"mean",
   "unauthorized_release":"mean",
   "completed":"mean",
   "refunded":"mean",
   "proof_ms":"mean",
   "arb_ms":"mean",
   "gas":"mean",
   "sol_cu":"mean",
   "disclosure_count":"mean"
  }
  available={name:agg for name,agg in columns.items() if name in df.columns}
  if available:
   df.groupby("method").agg(available).to_csv(Path(out)/"method_summary.csv")

 # E5 is a proof-cost experiment and has no protocol "method" column.
 if "variant" in df.columns:
  columns={
   "proof_ms":"mean",
   "proof_size":"mean",
   "verify_ms":"mean",
   "gas":"mean",
   "sol_cu":"mean"
  }
  available={name:agg for name,agg in columns.items() if name in df.columns}
  if available:
   df.groupby("variant").agg(available).to_csv(Path(out)/"zk_variant_summary.csv")

 # Preserve experiment-specific configuration summaries when present.
 for group_col,filename in [
  ("fault_rate","fault_summary.csv"),
  ("committee_size","committee_summary.csv"),
  ("byzantine_fraction","byzantine_summary.csv")
 ]:
  if group_col in df.columns:
   numeric=df.select_dtypes(include="number").columns.tolist()
   numeric=[c for c in numeric if c not in {"seed","credential"}]
   if numeric:
    df.groupby(group_col)[numeric].mean().to_csv(Path(out)/filename)
