# Additional Edge/Robustness Tests

import pytest

# --- Common edge cases ---

def test_empty_requests_all_policies():
    assert simulate_fifo(3, []) == 0
    assert simulate_lru(3, []) == 0
    assert simulate_optff(3, []) == 0

def test_zero_cache_always_miss():
    req = [1, 2, 1, 3, 1]
    assert simulate_fifo(0, req) == len(req)
    assert simulate_lru(0, req) == len(req)
    assert simulate_optff(0, req) == len(req)

def test_large_cache_no_evictions_all_policies():
    req = [1, 2, 3, 2, 1, 4, 5, 4]
    k = 10
    # misses are just the number of distinct items in order of first appearance
    assert simulate_fifo(k, req) == 5
    assert simulate_lru(k, req) == 5
    assert simulate_optff(k, req) == 5
)

# --- FIFO specific ---

def test_fifo_eviction_order_progresses_with_hits():
    """
    FIFO queue advances only on insertions, not hits.
    k=3, fill 1,2,3; hit 1; insert 4 should evict 1 (still oldest).
    """
    assert simulate_fifo(3, [1, 2, 3, 1, 4]) == 4  # misses: 1,2,3,4

def test_fifo_with_k2_alternating_pattern():
    """
    k=2: 1,2 fill; 3 evicts 1; 1 evicts 2; 2 evicts 3...
    requests: 1 2 3 1 2
    misses: 1,2,3,1,2 = 5
    """
    assert simulate_fifo(2, [1, 2, 3, 1, 2]) == 5

# --- LRU specific ---

def test_lru_no_eviction_when_reusing_two_items():
    """k=2 and only {1,2} used -> only first two misses."""
    assert simulate_lru(2, [1, 2, 1, 2, 1, 2, 2, 1]) == 2

def test_lru_recency_chain_eviction():
    """
    k=3: 1,2,3 fill; access 1 then 2 => LRU is 3; insert 4 evicts 3.
    requests: 1 2 3 1 2 4 3
    misses: 1,2,3,4,3 = 5
    """
    assert simulate_lru(3, [1, 2, 3, 1, 2, 4, 3]) == 5

# --- OPT (Belady / farthest-in-future) specific ---

def test_optff_k1_equivalent_to_fifo_lru():
    """With k=1, all policies behave the same (only last requested can be cached)."""
    req = [1, 2, 1, 2, 3, 2]
    assert simulate_optff(1, req) == simulate_fifo(1, req)
    assert simulate_optff(1, req) == simulate_lru(1, req)

def test_optff_evict_never_used_again():
    """
    k=2, requests: 1 2 3 1 2
    After 1,2 cached; request 3 => must evict either 1 or 2.
    Optimal evicts 2 (used at end) or 1 depending on future:
      future after inserting 3: sequence is 1,2.
      So evict 2? Actually 1 is used sooner than 2, so evict 2 (farthest).
    misses: 1,2,3 = 3
    """
    assert simulate_optff(2, [1, 2, 3, 1, 2]) == 3

def test_optff_strictly_better_than_fifo_on_classic_sequence():
    """
    Classic where OPT beats FIFO with k=3 (often used in paging examples).
    Just assert it's strictly better (fewer misses), not exact count.
    """
    req = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    k = 3
    assert simulate_optff(k, req) < simulate_fifo(k, req)

def test_optff_strictly_better_than_lru_on_classic_sequence():
    """Same sequence: OPT should beat LRU as well."""
    req = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    k = 3
    assert simulate_optff(k, req) < simulate_lru(k, req)
