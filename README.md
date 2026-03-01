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

*(Dom)*

### Question 1: Empirical Comparison
### Question 2: Bad Sequence for LRU or FIFO
### Question 3: Proof that OPTFF is Optimal
