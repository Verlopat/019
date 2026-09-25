from dataclasses import dataclass
from pathlib import Path
import hashlib,json

@dataclass(frozen=True)
class SanctionsSnapshot:
 source:str; snapshot_date:str; addresses:frozenset; file_hash:str; root:str

def load_snapshot(path=None):
 if path and Path(path).exists(): raw=Path(path).read_bytes(); addresses=frozenset(a.lower() for a in json.loads(raw).get("addresses",[]))
 else: raw=b"EMPTY-SYNTHETIC-SNAPSHOT"; addresses=frozenset()
 h=hashlib.sha256(raw).hexdigest(); root=hashlib.sha256("|".join(sorted(addresses)).encode()).hexdigest()
 return SanctionsSnapshot("frozen-local-snapshot","prototype",addresses,h,root)

def is_clear(address,s): return address.lower() not in s.addresses
