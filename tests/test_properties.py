from hypothesis import given,strategies as st
from sdhtlc.core import Decision
from sdhtlc.arbitration.committee import collusion_probability

@given(st.integers(min_value=3,max_value=15),st.floats(min_value=0,max_value=.5,allow_nan=False,allow_infinity=False))
def test_collusion_probability_is_bounded(k,q):
 assert 0 <= collusion_probability(k,q) <= 1

@given(st.integers(min_value=3,max_value=20))
def test_threshold_is_majority_or_more(k):
 from math import ceil
 assert ceil(k*2/3) >= (k//2+1)
