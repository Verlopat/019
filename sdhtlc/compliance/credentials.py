import hashlib,random
from sdhtlc.core import Credential,canonical_hash

def generate_credentials(n,seed):
 r=random.Random(seed); now=1750000000; out=[]
 for i in range(n):
  out.append(Credential(f"cred-{seed}-{i:06d}",f"issuer-{i%20}",r.choice(["EEA","US","GB","CH"]),r.choice([1,2,3]),now-r.randint(0,500000),now+r.randint(-100000,500000),r.random()<.03,r.randint(1,100),hashlib.sha256(f"wallet-{seed}-{i}".encode()).hexdigest(),hashlib.sha256(f"secret-{seed}-{i}".encode()).hexdigest()))
 return out

def dataset_hash(cs): return canonical_hash([c.__dict__ for c in cs])
