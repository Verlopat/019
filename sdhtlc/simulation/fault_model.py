from dataclasses import dataclass

@dataclass(frozen=True)
class FaultModel:
 provider_failure:float=0.0
 byzantine_fraction:float=0.0
 network_delay:float=.05
 timelock_margin:float=30.0
