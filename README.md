# Programming Assignment 2: Greedy Algorithms

## Authors
| Name | UFID |
|------|------|
| Tyler Pencinger | 86826331 |
| Dominick Dupuy | 39922039 |

---

## Overview
This project implements and compares three cache eviction policies on a given request sequence:

- **FIFO** — First-In, First-Out
- **LRU** — Least Recently Used
- **OPTFF** — Belady's Farthest-in-Future (optimal offline)

---

## Repository Structure
```
cache-eviction/
├── src/
│   └── cache.py         # Main implementation (FIFO, LRU, OPTFF)
├── data/
│   ├── input1.in        # Test case 1 (k=3, m=20)
│   ├── input1.out       # Expected output for input1
│   ├── input2.in        # Test case 2 (k=3, m=60, sequential scan)
│   └── input3.in        # Test case 3 (k=4, m=50, locality of reference)
├── tests/
│   └── test_cache.py    # Unit tests for all three policies
└── README.md
```

---

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only standard library)

---

## How to Run
```bash
python src/cache.py <input_file>
```

**Example:**
```bash
python src/cache.py data/input1.in
```

**Expected output:**
```
FIFO  : 17
LRU   : 18
OPTFF : 10
```

---

## Input Format
```
k m
r1 r2 r3 ... rm
```

- `k` = cache capacity (integer ≥ 1)
- `m` = number of requests
- `r1 ... rm` = space-separated integer item IDs

---

## Written Component


### Question 1: Empirical Comparison

| Input File | k | m  | FIFO | LRU | OPTFF |
|------------|---|----|------|-----|-------|
| input1.in  | 3 | 20 | 17   | 18  | 10    |
| input2.in  | 3 | 60 | 60   | 60  | 38    |
| input3.in  | 4 | 50 | 21   | 21  | 15    |

OPTFF has the fewest misses in all three cases since it has full knowledge of future requests, and it always evicts the optimal item. FIFO and LRU perform in a similar way, with neither consistently outperforming the other one across all the inputs.

### Question 2: Bad Sequence for LRU or FIFO

Yes, such a sequence exists. Example:

`1 2 3 4 1 2 5 1 2 3 4 5`

For `k = 3`:
- FIFO misses = 9
- LRU misses = 10
- OPTFF misses = 7

So OPTFF is strictly better than both FIFO and LRU on this sequence.

Reasoning:
- The sequence creates conflicts where online policies evict items that will be needed soon.
- OPTFF uses future knowledge and evicts the item needed farthest in the future, preserving near-future hits.

### Question 3: Proof that OPTFF is Optimal

Let `S = r1, r2, ..., rm` be a fixed request sequence and cache size `k`.
Let `O` be OPTFF, and let `A` be any offline algorithm.

Consider the first time `t` where `A` and `O` make different eviction choices (all earlier choices are the same). At time `t`, both caches contain the same set before eviction. Suppose:
- `O` evicts page `x` (whose next use is farthest in the future, or never),
- `A` evicts page `y != x`.

Construct algorithm `A'` that is identical to `A` except at time `t`, where it evicts `x` instead of `y`, and then behaves like `A` after that with this swapped role until one of `x` or `y` is requested.

Key fact:
- By definition of OPTFF, next-use(`x`) is not earlier than next-use(`y`).
- Therefore, before `y` is requested, neither algorithm is harmed by having `y` kept instead of `x`.
- If one of `{x, y}` is requested first, it is `y` (or they are never used again). So replacing `A`'s choice with `O`'s cannot increase misses up to that point.
- After that first request to `y`, caches can be synchronized again without increasing total misses.

Thus `A'` has no more misses than `A`, and now agrees with `O` for one more eviction decision.
Repeat this exchange step for every disagreement. Eventually we transform `A` into `O` without increasing misses.

Therefore:
`misses(O) <= misses(A)` for every offline algorithm `A` on every sequence.
So OPTFF is optimal.
