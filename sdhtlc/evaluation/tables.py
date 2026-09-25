from pathlib import Path
def write_tables(df,out="results/processed"):
 Path(out).mkdir(parents=True,exist_ok=True)
 df.groupby("method").agg({"atomicity_violation":"mean","unauthorized_release":"mean","completed":"mean","refunded":"mean","proof_ms":"mean","arb_ms":"mean","gas":"mean","sol_cu":"mean","disclosure_count":"mean"}).to_csv(Path(out)/"method_summary.csv")
