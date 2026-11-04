import time
import statistics
import networkx as nx

# =====================================================================
# 1. N-QUEENS BACKTRACKING (Scanning, Used-Marks, Bitmasks)
# =====================================================================

def nqueens_scan(N):
    """1. SCANNING: Əvvəlki təyinatları tək-tək skan edir (O(N) check)."""
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
    """2. USED-MARKS: Sütun və diaqonalları Set/Array ilə izləyir (O(1) check)."""
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
    """3. BITMASKS: Bit əməliyyatları ilə tam optimallaşdırılmış yoxlama."""
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
    """1. SCANNING: Qonşuları tək-tək skan edərək rəng konfliktini yoxlayır."""
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
    """2. USED-MARKS: Hər təpə üçün istifadə olunmuş rəngləri Set ilə saxlayır."""
    V = len(adj_matrix)
    colors = [-1] * V
    neighbor_colors = [set() for _ in range(V)]
    nodes_visited = 0

    def backtrack(v):
        nonlocal nodes_visited
        nodes_visited += 1
        if v == V:
            return True

        for c in range(K):
            if c not in neighbor_colors[v]:
                colors[v] = c
                added_neighbors = []
                for u in range(V):
                    if adj_matrix[v][u]:
                        if c not in neighbor_colors[u]:
                            neighbor_colors[u].add(c)
                            added_neighbors.append(u)

                if backtrack(v + 1):
                    return True

                colors[v] = -1
                for u in added_neighbors:
                    neighbor_colors[u].remove(c)

        return False

    success = backtrack(0)
    return success, colors if success else None, nodes_visited


def graph_coloring_bitmask(adj_matrix, K):
    """3. BITMASKS: Qonşu rəngləri bitmask (1 << color) ilə izləyir."""
    V = len(adj_matrix)
    colors = [-1] * V
    neighbor_masks = [0] * V
    nodes_visited = 0

    def backtrack(v):
        nonlocal nodes_visited
        nodes_visited += 1
        if v == V:
            return True

        for c in range(K):
            color_bit = 1 << c
            if not (neighbor_masks[v] & color_bit):
                colors[v] = c
                updated_neighbors = []
                for u in range(V):
                    if adj_matrix[v][u] and not (neighbor_masks[u] & color_bit):
                        neighbor_masks[u] |= color_bit
                        updated_neighbors.append(u)

                if backtrack(v + 1):
                    return True

                colors[v] = -1
                for u in updated_neighbors:
                    neighbor_masks[u] &= ~color_bit

        return False

    success = backtrack(0)
    return success, colors if success else None, nodes_visited


# =====================================================================
# 3. VERİFİKASİYA (CORRECTNESS ORACLES / VALIDATORS)
# =====================================================================

N_QUEENS_KNOWN_SOLUTIONS = {
    4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352, 10: 724
}

def validate_graph_coloring(adj_matrix, colors):
    """Qrafın k-rənglənməsinin düzgünlüyünü yoxlayan müstəqil orakul."""
    if colors is None:
        return True
    V = len(adj_matrix)
    for u in range(V):
        for v in range(u + 1, V):
            if adj_matrix[u][v] and colors[u] == colors[v]:
                return False
    return True


# =====================================================================
# 4. BENÇMARK VƏ EXPERIMENTAL PROTOCOL (Timing Rigour)
# =====================================================================

def benchmark_function(func, *args, runs=7):
    """1 untimed warm-up + repeated timed runs -> Median Time."""
    _ = func(*args)

    times = []
    last_res = None
    for _ in range(runs):
        start = time.perf_counter()
        last_res = func(*args)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # ms

    median_time = statistics.median(times)
    return last_res, median_time


# =====================================================================
# 5. İCRA VƏ NƏTİCƏLƏR (GOOGLE COLAB)
# =====================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PART 1: N-QUEENS BENCHMARK (N=8)")
    print("=" * 60)
    N = 8
    expected = N_QUEENS_KNOWN_SOLUTIONS[N]

    methods_nq = [
        ("Scanning", nqueens_scan),
        ("Used-marks", nqueens_used_marks),
        ("Bitmasks", nqueens_bitmask)
    ]

    for name, fn in methods_nq:
        (sols, nodes), med_t = benchmark_function(fn, N)
        valid = (sols == expected)
        time_per_node = (med_t / nodes) * 1000 if nodes > 0 else 0
        print(f"[{name:10s}] Həll: {sols} | Ziyarət: {nodes:6d} | "
              f"Median Vaxt: {med_t:6.3f} ms | Qovşaq başı: {time_per_node:5.3f} µs | Orakul: {valid}")

    print("\n" + "=" * 60)
    print("PART 2: REAL GRAPH k-COLORING (Dolphins Dataset - dolphins.gml)")
    print("=" * 60)
    
    # Google Colab-dakı dolphins.gml faylını oxuyuruq
    try:
        G = nx.read_gml("dolphins.gml")
        # Gml fayllarında bəzən node adları string ola bilər, onları integer indeksə keçiririk
        G = nx.convert_node_labels_to_integers(G)
        adj_matrix = nx.to_numpy_array(G, dtype=int).tolist()
        V = len(adj_matrix)
        K = 4  # Dolphins qrafı üçün 4 rəng testi (və ya 5)

        print(f"Dataset uğurla oxundu! Təpə nöqtəsi (V): {V} | Tillər (E): {G.number_of_edges()}")

        methods_gc = [
            ("Scanning", graph_coloring_scan),
            ("Used-marks", graph_coloring_used_marks),
            ("Bitmasks", graph_coloring_bitmask)
        ]

        for name, fn in methods_gc:
            (success, colors, nodes), med_t = benchmark_function(fn, adj_matrix, K)
            valid = validate_graph_coloring(adj_matrix, colors)
            time_per_node = (med_t / nodes) * 1000 if nodes > 0 else 0
            print(f"[{name:10s}] Tapıldı: {str(success):5s} | Ziyarət: {nodes:6d} | "
                  f"Median Vaxt: {med_t:6.3f} ms | Qovşaq başı: {time_per_node:5.3f} µs | Orakul: {valid}")

    except FileNotFoundError:
        print("XƏTA: 'dolphins.gml' faylı tapılmadı!")
        print("Zəhmət olmasa sol paneldən (Files bölməsindən) faylı Colab-a yüklədiyinizə əmin olun.")
