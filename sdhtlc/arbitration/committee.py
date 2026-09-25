import hashlib,random
from dataclasses import dataclass

@dataclass
class Member:
 member_id:str; stake:float; malicious:bool=False; active:bool=True

def select_committee(members,k,seed,dispute_id):
 eligible=[m for m in members if m.active and m.stake>0]; r=random.Random(int(hashlib.sha256(f"{seed}:{dispute_id}".encode()).hexdigest(),16))
 return r.sample(eligible,k)

def collusion_probability(k,q,ratio=2/3):
 from math import comb,ceil
 t=ceil(k*ratio); return sum(comb(k,j)*q**j*(1-q)**(k-j) for j in range(t,k+1))
