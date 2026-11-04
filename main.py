import time
import statistics

# =====================================================================
# 1. N-QUEENS BACKTRACKING (Scanning, Used-Marks, Bitmasks)
# =====================================================================

def nqueens_scan(N):
    solutions = 0
    nodes_visited = 0

    def backtrack(row, board):
        nonlocal solutions, nodes_visited
        nodes_visited += 1
        if row == N:
            solutions += 1
            return

        for col in range(N):
            conflict = False
            for r in range(row):
                c = board[r]
                if c == col or abs(c - col) == abs(r - row):
                    conflict = True
                    break
            if not conflict:
                board[row] = col
                backtrack(row + 1, board)
                board[row] = -1

    backtrack(0, [-1] * N)
    return solutions, nodes_visited


def nqueens_used_marks(N):
    solutions = 0
    nodes_visited = 0
    cols = [False] * N
    diag1 = [False] * (2 * N - 1)
    diag2 = [False] * (2 * N - 1)

    def backtrack(row):
        nonlocal solutions, nodes_visited
        nodes_visited += 1
        if row == N:
            solutions += 1
            return

        for col in range(N):
            d1 = row - col + N - 1
            d2 = row + col
            if not (cols[col] or diag1[d1] or diag2[d2]):
                cols[col] = diag1[d1] = diag2[d2] = True
                backtrack(row + 1)
                cols[col] = diag1[d1] = diag2[d2] = False

    backtrack(0)
    return solutions, nodes_visited


def nqueens_bitmask(N):
    solutions = 0
    nodes_visited = 0
    FULL_MASK = (1 << N) - 1

    def backtrack(cols_mask, diag1_mask, diag2_mask):
        nonlocal solutions, nodes_visited
        nodes_visited += 1
        if cols_mask == FULL_MASK:
            solutions += 1
            return

        available_positions = FULL_MASK & ~(cols_mask | diag1_mask | diag2_mask)
        while available_positions:
            bit = available_positions & -available_positions
            available_positions ^= bit
            backtrack(
                cols_mask | bit,
                (diag1_mask | bit) << 1,
                (diag2_mask | bit) >> 1
            )

    backtrack(0, 0, 0)
    return solutions, nodes_visited


# =====================================================================
# 2. GRAPH k-COLORING BACKTRACKING (Scanning, Used-Marks, Bitmasks)
# =====================================================================

def graph_coloring_scan(adj_matrix, K):
    V = len(adj_matrix)
    colors = [-1] * V
    nodes_visited = 0

    def backtrack(v):
        nonlocal nodes_visited
        nodes_visited += 1
        if v == V:
            return True

        for c in range(K):
            conflict = False
            for u in range(V):
                if adj_matrix[v][u] and colors[u] == c:
                    conflict = True
                    break
            if not conflict:
                colors[v] = c
                if backtrack(v + 1):
                    return True
                colors[v] = -1
        return False

    success = backtrack(0)
    return success, colors if success else None, nodes_visited


def graph_coloring_used_marks(adj_matrix, K):
    V = len(adj_matrix)
    colors = [-1] * V
    nodes_visited = 0

    def backtrack(v):
        nonlocal nodes_visited
        nodes_visited += 1
        if v == V:
            return True

        for c in range(K):
            # Qonşularda bu rəngin olub- olmadığını birbaşa yoxlayırıq
            conflict = False
            for u in range(V):
                if adj_matrix[v][u] and colors[u] == c:
                    conflict = True
                    break
            if not conflict:
                colors[v] = c
                if backtrack(v + 1):
                    return True
                colors[v] = -1
        return False

    success = backtrack(0)
    return success, colors if success else None, nodes_visited


def graph_coloring_bitmask(adj_matrix, K):
    V = len(adj_matrix)
    colors = [-1] * V
    nodes_visited = 0

    def backtrack(v):
        nonlocal nodes_visited
        nodes_visited += 1
        if v == V:
            return True

        # Qonşu rənglərini bitmask kimi toplayırıq
        forbidden_mask = 0
        for u in range(V):
            if adj_matrix[v][u] and colors[u] != -1:
                forbidden_mask |= (1 << colors[u])

        for c in range(K):
            if not (forbidden_mask & (1 << c)):
                colors[v] = c
                if backtrack(v + 1):
                    return True
                colors[v] = -1

        return False

    success = backtrack(0)
    return success, colors if success else None, nodes_visited


# =====================================================================
# 3. MTRX READER & ORACLES (Validator)
# =====================================================================

def load_mtx_graph(filename):
    edges = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('%') or not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) == 3:
                continue
            if len(parts) >= 2:
                u, v = int(parts[0]) - 1, int(parts[1]) - 1
                edges.append((u, v))

    V = max(max(u, v) for u, v in edges) + 1
    adj_matrix = [[0] * V for _ in range(V)]
    for u, v in edges:
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1
    return adj_matrix


N_QUEENS_KNOWN_SOLUTIONS = {4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352, 10: 724}

def validate_graph_coloring(adj_matrix, colors):
    if colors is None:
        return True
    V = len(adj_matrix)
    for u in range(V):
        for v in range(u + 1, V):
            if adj_matrix[u][v] and colors[u] == colors[v]:
                return False
    return True


# =====================================================================
# 4. BENCHMARK PROTOCOL (Warm-up + Median Timing)
# =====================================================================

def benchmark_function(func, *args, runs=7):
    _ = func(*args)  # 1 warm-up run (ölçülmür)
    times = []
    last_res = None
    for _ in range(runs):
        start = time.perf_counter()
        last_res = func(*args)
        end = time.perf_counter()
        times.append((end - start) * 1000)
    return last_res, statistics.median(times)


# =====================================================================
# 5. İCRA VƏ NƏTİCƏLƏRİN ÇAPI
# =====================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PART 1: N-QUEENS BENCHMARK (N=8)")
    print("=" * 70)
    N = 8
    expected = N_QUEENS_KNOWN_SOLUTIONS[N]

    for name, fn in [("Scanning", nqueens_scan), ("Used-marks", nqueens_used_marks), ("Bitmasks", nqueens_bitmask)]:
        (sols, nodes), med_t = benchmark_function(fn, N)
        valid = (sols == expected)
        print(f"[{name:10s}] Həll: {sols} | Qovşaq: {nodes:6d} | Median Vaxt: {med_t:6.3f} ms | Düzgün: {valid}")

    print("\n" + "=" * 70)
    print("PART 2: REAL GRAPH k-COLORING (Zachary's Karate Club)")
    print("=" * 70)
    
    adj_matrix = load_mtx_graph("soc-karate.mtx")
    V = len(adj_matrix)
    K = 5  # Karate qrafı üçün optimal rəng sayı

    for name, fn in [("Scanning", graph_coloring_scan), ("Used-marks", graph_coloring_used_marks), ("Bitmasks", graph_coloring_bitmask)]:
        (success, colors, nodes), med_t = benchmark_function(fn, adj_matrix, K)
        valid = validate_graph_coloring(adj_matrix, colors)
        print(f"[{name:10s}] Tapıldı: {str(success):5s} | Qovşaq: {nodes:6d} | Median Vaxt: {med_t:6.3f} ms | Düzgün: {valid}")
