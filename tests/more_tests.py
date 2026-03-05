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
