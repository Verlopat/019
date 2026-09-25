"""Freeze an OFAC sanctions file into a reproducible local snapshot.
Download the exact file from the OFAC Sanctions List Service, then run:
python scripts/freeze_ofac.py path/to/sdn.json --date 2026-09-25
The source hash is stored alongside the snapshot. OFAC publishes file hashes for content assurance.
"""
import argparse,hashlib,json
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument("source"); ap.add_argument("--date",required=True); ap.add_argument("--output",default="data/sanctions/ofac_snapshot.json"); a=ap.parse_args()
raw=Path(a.source).read_bytes(); h=hashlib.sha256(raw).hexdigest()
try:
 obj=json.loads(raw); addresses=[]
 for entry in obj.get("entries",obj if isinstance(obj,list) else []):
  for k,v in entry.items():
   if "digital currency address" in str(k).lower(): addresses.append(str(v).strip())
except Exception:
 addresses=[]
out={"source":"OFAC Sanctions List Service","snapshot_date":a.date,"source_file_sha256":h,"addresses":sorted(set(addresses))}
Path(a.output).parent.mkdir(parents=True,exist_ok=True); Path(a.output).write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps({"output":a.output,"sha256":h,"addresses":len(out["addresses"])},indent=2))
