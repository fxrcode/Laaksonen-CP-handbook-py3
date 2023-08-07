# Chap 5: Complete search -> Pruning the search
"""
metacognition: 
takeaway: 
- C++ is way faster than Python (using 3.11.4) !!!!
- how to do pruning?
    - when left/right on_path, but not up or down, then you split (so you should prune)
    - for deadend optimization: means you have to goto that spot as next position

---
There are 88418 paths in a 7×7 grid from the upper-left square to the lower-left square. Each path corresponds to a 48
-character description consisting of characters D (down), U (up), L (left) and R (right).

For example, the path (fig 0) corresponds to the description DRURRRRRDDDLUULDDDLDRRURDDLLLLLURULURRUULDLLDDDD.

You are given a description of a path which may also contain characters ? (any direction). Your task is to calculate the number of paths that match the description.

Input

The only input line has a 48
-character string of characters ?, D, U, L and R.

Output

Print one integer: the total number of paths.

Example

Input:
??????R??????U??????????????????????????LD????D?

Output:
201

Input:
???????????LUULDDDLDRRURDDLLLLLURULURRUULDLLDDDD
Output:
1

TIMING:
$ time python ch5_complete_search.py (opt: 3 possible deadend)
??????R??????U??????????????????????????LD????D?
201
python ch5_complete_search.py  27.36s user 0.15s system 97% cpu 28.150 total

$ time python ch5_complete_search.py (opt: 4 possible deadend)
??????R??????U??????????????????????????LD????D?
201
python ch5_complete_search.py  19.38s user 0.27s system 85% cpu 22.960 total

$ time python ch5_complete_search.py (no possible deadend)
??????R??????U??????????????????????????LD????D?
201
python ch5_complete_search.py  224.36s user 1.11s system 99% cpu 3:47.36 total

$ time python ch5_complete_search.py (opt: 4 possible deadend)
????U???????????D???????????????????????????????
6665
python ch5_complete_search.py  15.43s user 0.06s system 95% cpu 16.268 total

$ time python ch5_complete_search.py (opt: 4 possible deadend)
????????????????????????????????????????????????
88418
python ch5_complete_search.py  297.71s user 2.01s system 95% cpu 5:15.01 total
"""
from collections import defaultdict
import time
import sys

ip = sys.stdin.readline
N = 7


def main():
    DIR = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # U,R,D,L
    PATH_LEN = N * N - 1
    p = [0 for _ in range(PATH_LEN)]
    on_path = defaultdict(bool)

    def try_path(path_idx, cur_r, cur_c) -> int:
        if not (0 <= cur_r < N and 0 <= cur_c < N):
            return 0
        # optimization #3
        if (on_path[(cur_r, cur_c - 1)] and on_path[(cur_r, cur_c + 1)]) and (
            not on_path[(cur_r - 1, cur_c)] and not on_path[(cur_r + 1, cur_c)]
        ):
            return 0
        if (on_path[(cur_r - 1, cur_c)] and on_path[(cur_r + 1, cur_c)]) and (
            not on_path[(cur_r, cur_c - 1)] and not on_path[(cur_r, cur_c + 1)]
        ):
            return 0

        if (cur_r, cur_c) == (N - 1, 0):
            # reached endpoint before visiting all
            if path_idx == PATH_LEN:
                return 1
            return 0

        if path_idx == PATH_LEN:
            return 0

        ret = 0
        on_path[(cur_r, cur_c)] = True

        # turn already determined
        if p[path_idx] < 4:
            dx, dy = DIR[p[path_idx]]
            nxt_r, nxt_c = cur_r + dx, cur_c + dy
            if not on_path[(nxt_r, nxt_c)]:
                ret += try_path(path_idx + 1, nxt_r, nxt_c)
        elif (
            on_path[(cur_r, cur_c - 2)]
            and (on_path[(cur_r - 1, cur_c - 1)] or on_path[(cur_r + 1, cur_c - 1)])
            and not on_path[(cur_r, cur_c - 1)]
        ):
            # potential deadend on the left
            nxt_r, nxt_c = cur_r, cur_c - 1
            ret += try_path(path_idx + 1, nxt_r, nxt_c)
        elif (
            on_path[(cur_r, cur_c + 2)]
            and (on_path[(cur_r - 1, cur_c + 1)] or on_path[(cur_r + 1, cur_c + 1)])
            and not on_path[(cur_r, cur_c + 1)]
        ):
            # potential deadend on the right
            nxt_r, nxt_c = cur_r, cur_c + 1
            ret += try_path(path_idx + 1, nxt_r, nxt_c)
        elif (
            on_path[(cur_r - 2, cur_c)]
            and (on_path[(cur_r - 1, cur_c - 1)] or on_path[(cur_r - 1, cur_c + 1)])
            and not on_path[(cur_r - 1, cur_c)]
        ):
            # potential deadend on the upwards
            nxt_r, nxt_c = cur_r - 1, cur_c
            ret += try_path(path_idx + 1, nxt_r, nxt_c)
        elif (
            on_path[(cur_r + 2, cur_c)]
            and (on_path[(cur_r + 1, cur_c - 1)] or on_path[(cur_r + 1, cur_c + 1)])
            and not on_path[(cur_r + 1, cur_c)]
        ):
            # potential deadend on the downwards
            nxt_r, nxt_c = cur_r + 1, cur_c
            ret += try_path(path_idx + 1, nxt_r, nxt_c)
        else:
            # iterate through all 4 possible turns
            for dx, dy in DIR:
                nxt_r, nxt_c = cur_r + dx, cur_c + dy
                if on_path[(nxt_r, nxt_c)]:
                    continue
                ret += try_path(path_idx + 1, nxt_r, nxt_c)
        # reset and return (aka Backtracking)
        on_path[(cur_r, cur_c)] = False
        return ret

    def mn():
        line = ip().strip()
        # convert path str into index
        for i, c in enumerate(line):
            if c == "U":
                p[i] = 0
            elif c == "R":
                p[i] = 1
            elif c == "D":
                p[i] = 2
            elif c == "L":
                p[i] = 3
            else:  # ?
                p[i] = 4

        start_idx = 0
        start_r = start_c = 0
        ans = try_path(start_idx, start_r, start_c)
        print(ans)

    return mn()


main()


def num_grid_paths_SLOW(N: int):
    def bt(x, y, vis, path, paths):
        # base
        # if x==y==N-1 and p not in paths and len(p) == N*N:
        if (x, y) == t:
            if len(path) == N**2:
                # paths.add(p)
                # print(p)
                return 1
            else:
                return 0
        # relation
        ans = 0
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            xx, yy = x + dx, y + dy
            if not (0 <= xx < N and 0 <= yy < N) or (xx, yy) in vis:
                continue
            if (
                (x == 0 and dy == -1)
                or (x == N - 1 and dy == -1)
                or (y == 0 and dx == -1)
                or (y == N - 1 and dx == -1)
            ):
                continue
            else:
                vis.add((xx, yy))
                path.append((xx, yy))
                ans += bt(xx, yy, vis, path, paths)
                path.pop()
                vis.remove((xx, yy))
        return ans

    s, t = (0, 0), (N - 1, N - 1)
    vis = set(s)
    paths = set()
    path = [s]
    t0 = time.perf_counter()
    res = bt(0, 0, vis, path, paths)
    t1 = time.perf_counter()
    print(res)
    print(f"spent {t1-t0=}")


# num_grid_paths_SLOW(5)
