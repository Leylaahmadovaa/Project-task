# University Project T17: Conflict-Checking Optimization in Backtracking Algorithms
## N-Queens & Graph $k$-Coloring Benchmark

This project demonstrates and benchmarks three different conflict-checking strategies (**Scanning**, **Used-marks**, and **Bitmasks**) within a standard Backtracking framework. The performance of these methods is evaluated on two classic NP-complete/hard computational problems:

1. **N-Queens Problem** ($N=8$)
2. **Graph $k$-Coloring** on a real-life dataset (**Zachary's Karate Club Graph**, $K=5$)

---

## 📌 Table of Contents
- [Project Overview](#project-overview)
- [Conflict-Checking Strategies](#conflict-checking-strategies)
- [Dataset Information](#dataset-information)
- [Experimental Methodology](#experimental-methodology)
- [Execution & Setup](#execution--setup)
- [Project Structure & Results](#project-structure--results)

---

## 🔍 Project Overview

Backtracking is a systematic method for exploring space trees to find solutions to constraint satisfaction problems (CSPs). The primary bottleneck in backtracking is evaluating whether adding a new candidate creates a constraint violation.

This repository compares:
* **N-Queens:** Placing $N$ non-attacking queens on an $N \times N$ chessboard.
* **Graph $k$-Coloring:** Assigning colors to vertices of an undirected simple graph such that no two adjacent vertices share the same color.

Both problems share an identical algorithmic foundation: testing candidate feasibility prior to recursive expansion.

---

## 🛠 Conflict-Checking Strategies

1. **Scanning ($O(N)$ / $O(V)$):**
   * Dynamically iterates over previously placed entities or neighbors to check for conflicts on the fly.
2. **Used-marks ($O(1)$ lookup):**
   * Maintains explicit state tracking structures (e.g., boolean arrays or hash sets) to record already occupied columns, diagonals, or neighbor colors.
3. **Bitmasks (Bitwise Parallelism):**
   * Encodes occupied states as integer bitmasks. Uses fast bitwise logic (`AND`, `OR`, `XOR`, shifts) to evaluate available slots instantly.

---

## 📊 Dataset Information

* **Name:** Zachary's Karate Club (`soc-karate.mtx`)
* **Source:** Wayne W. Zachary (1977), Matrix Market format (`.mtx`)
* **Graph Type:** Undirected, unweighted simple graph
* **Vertices ($V$):** 34
* **Edges ($E$):** 78
* **Chromatic Number ($K$):** $K=5$ (for full valid assignment in basic backtracking order)

---

## ⏱ Experimental Methodology

To eliminate environmental variance and modern CPU frequency scaling artifacts, the execution framework implements rigorous benchmarking protocols:
1. **Separation of I/O:** Dataset parsing and data matrix construction are excluded from execution timing.
2. **Warm-Up Run:** One initial untimed run is performed per algorithm to prime CPU caches and JIT interpreters.
3. **Repeated Timed Runs:** Algorithms are executed for 7 iterations using `time.perf_counter()`.
4. **Median Aggregation:** Results report the median runtime across repetitions to neutralize OS background jitter.
5. **Correctness Oracles:** Independent verification functions validate whether generated solutions meet all domain constraints (e.g., matching known $N$-Queens solution counts or validating graph edge-color non-collision).

---

## 🚀 Execution & Setup

### Running in Google Colab / Local Python Environment

1. Ensure Python 3.x is installed.
2. Place the `soc-karate.mtx` file in the working directory (or rely on the embedded parser script).
3. Execute the main benchmarking script:

```bash
python main.py
```

---

## 📈 Sample Performance Output

| Problem Domain | Method | Visited Nodes | Median Time (ms) | Oracle Status |
| :--- | :--- | :---: | :---: | :---: |
| **N-Queens ($N=8$)** | Scanning | 2057 | ~7.54 ms | `True` |
| **N-Queens ($N=8$)** | Used-marks | 2057 | ~2.10 ms | `True` |
| **N-Queens ($N=8$)** | Bitmasks | 2057 | ~0.91 ms | `True` |
| **Graph $k$-Coloring ($K=5$)** | Scanning | Variable | Measured | `True` |
| **Graph $k$-Coloring ($K=5$)** | Used-marks | Variable | Measured | `True` |
| **Graph $k$-Coloring ($K=5$)** | Bitmasks | Variable | Measured | `True` |

---

## 🎓 Academic Defense Notes (Summary for Evaluation)
* **Backtracking Tree Equality:** Notice how the number of visited nodes remains identical across all three strategies for a given problem. The algorithms traverse the exact same search tree; the performance improvement stems entirely from reducing **per-node evaluation overhead**.
* **Bitmask Dominance:** Bitwise manipulation minimizes CPU branch mispredictions and eliminates dynamic memory/array index lookups during constraint checking.