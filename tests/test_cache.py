
# Run with: python -m pytest tests/test_cache.py -v


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cache import simulate_fifo, simulate_lru, simulate_optff

# FIFO Tests

def test_fifo_all_hits():
    """Cache is large enough to hold everything so no evictions."""
    assert simulate_fifo(5, [1, 2, 3, 1, 2, 3]) == 3  

def test_fifo_all_misses():
    """k=1, all distinct items so every request is a miss."""
    assert simulate_fifo(1, [1, 2, 3, 4, 5]) == 5

def test_fifo_basic_eviction():
    """Classic FIFO: 1,2,3 fill cache; 4 evicts 1 (oldest)."""
    # requests: 1 2 3 4 1
    # cache after each:
    #   1 -> {1}       miss
    #   2 -> {1,2}     miss
    #   3 -> {1,2,3}   miss
    #   4 -> {2,3,4}   miss (evict 1)
    #   1 -> {3,4,1}   miss (evict 2)
    assert simulate_fifo(3, [1, 2, 3, 4, 1]) == 5

def test_fifo_repeated_access_does_not_reset_order():
    """FIFO does NOT reset an item's position on re-access."""
    # k=2: 1,2 fill cache; access 1 again (hit, no reset); 3 evicts 1 (still oldest)
    assert simulate_fifo(2, [1, 2, 1, 3]) == 3

def test_fifo_k1():
    assert simulate_fifo(1, [1, 1, 1, 2, 2, 1]) == 3

# LRU Tests

def test_lru_all_hits():
    assert simulate_lru(5, [1, 2, 3, 1, 2, 3]) == 3

def test_lru_all_misses():
    assert simulate_lru(1, [1, 2, 3, 4, 5]) == 5

def test_lru_basic_eviction():
    # k=2: 1,2 fill; 3 evicts LRU=1; 2 is hit; 1 evicts LRU=3
    # requests: 1 2 3 2 1
    # 1 miss {1}
    # 2 miss {1,2}
    # 3 miss {2,3}  evict 1 (LRU)
    # 2 hit  {3,2}
    # 1 miss {2,1}  evict 3 (LRU)
    assert simulate_lru(2, [1, 2, 3, 2, 1]) == 3

def test_lru_recency_resets_on_access():
    """LRU DOES reset recency on re-access — unlike FIFO."""
    # k=2: 1,2 fill; access 1 (refreshes 1); 3 evicts 2 (now LRU)
    # requests: 1 2 1 3
    # 1 miss {1}
    # 2 miss {1,2}
    # 1 hit  {2,1}  — 1 is now MRU, 2 is LRU
    # 3 miss {1,3}  evict 2
    assert simulate_lru(2, [1, 2, 1, 3]) == 3

def test_lru_k1():
    assert simulate_lru(1, [1, 1, 1, 2, 2, 1]) == 3

def test_optff_never_worse_than_fifo():
    requests = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    k = 3
    assert simulate_optff(k, requests) <= simulate_fifo(k, requests)

def test_optff_never_worse_than_lru():
    requests = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    k = 3
    assert simulate_optff(k, requests) <= simulate_lru(k, requests)

def test_optff_optimal_on_known_sequence():
    # k=2, requests: 1 2 1 3 2
    # Optimal evicts 3 after inserting it (never used again)
    # misses: 1,2,3 = 3
    assert simulate_optff(2, [1, 2, 1, 3, 2]) == 3