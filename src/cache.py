import sys
from collections import deque, OrderedDict


def simulate_fifo(k, requests):

    cache = set()
    queue = deque()
    misses = 0

    for req in requests:
        if req in cache:
    
            pass
        else:
            misses += 1
            if len(cache) < k:
                cache.add(req)
                queue.append(req)
            else:
                
                evict = queue.popleft()
                cache.remove(evict)
                cache.add(req)
                queue.append(req)

    return misses


def simulate_lru(k, requests):
    
    cache = OrderedDict()
    misses = 0

    for req in requests:
        if req in cache:
            
            cache.move_to_end(req)
        else:
            misses += 1
            if len(cache) >= k:
                
                cache.popitem(last=False)
            cache[req] = True

    return misses


def simulate_optff(k, requests):
   

    # TODO (DOM): Implement this function.
    # Build a lookup: for each position i, next_use[i] = next index where requests[i] appears
    # (or infinity if it never appears again)

    n = len(requests)

   
    next_use = [float('inf')] * n
    last_seen = {}
    for i in range(n - 1, -1, -1):
        r = requests[i]
        if r in last_seen:
            next_use[i] = last_seen[r]
        last_seen[r] = i

    cache = {} 
    misses = 0

    for i, req in enumerate(requests):
        if req in cache:
            
            cache[req] = next_use[i]
        else:
            misses += 1
            
            nu = next_use[i]
            if len(cache) < k:
                cache[req] = nu
            else:
            
                evict = max(cache, key=lambda x: cache[x])
                del cache[evict]
                cache[req] = nu

    return misses


def main():
    if len(sys.argv) < 2:
        print("Usage: python cache.py <input_file>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        first_line = f.readline().split()
        k, m = int(first_line[0]), int(first_line[1])
        requests = list(map(int, f.readline().split()))

    assert len(requests) == m, f"Expected {m} requests, got {len(requests)}"

    fifo_misses  = simulate_fifo(k, requests)
    lru_misses   = simulate_lru(k, requests)
    optff_misses = simulate_optff(k, requests)

    print(f"FIFO  : {fifo_misses}")
    print(f"LRU   : {lru_misses}")
    print(f"OPTFF : {optff_misses}")


if __name__ == "__main__":
    main()