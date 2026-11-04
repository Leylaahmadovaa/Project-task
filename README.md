# Project Work 1: T17 - N-Queens and Graph $k$-Coloring Optimization

## 📌 Project Overview
This project investigates the performance impact of different **conflict-checking strategies** (*Scanning*, *Used-marks*, and *Bitmasks*) across two classic combinatorial optimization problems:
1. **N-Queens Problem:** Evaluated on the $N=8$ board configuration.
2. **Real-Life Graph $k$-Coloring Problem:** Evaluated on the **Dolphins social network dataset** (`dolphins.gml`, containing 62 nodes and 159 edges).

The core objective is to measure how advanced conflict representation structures (like bitwise operations and state-tracking arrays) reduce CPU overhead and node exploration times during Backtracking search.

---

## 🛠️ Repository Contents
* `main.py`: The complete, production-ready Python script implementing all three conflict-checking strategies for both N-Queens and Graph $k$-Coloring, complete with verification oracles and timing rigor protocols.
* `dolphins.gml`: The real-life unweighted, undirected simple graph dataset representing bottlenose dolphins' interactions.
* `README.md`: Project documentation and instructions.

---

## 🚀 How to Run in Google Colab

1. **Upload Files:**
   * Open [Google Colab](https://colab.research.google.com/).
   * Upload the `dolphins.gml` dataset file into the Colab file explorer panel (left sidebar).
   * Copy the code from `main.py` into a code cell.

2. **Execute the Script:**
   * Run the cell using `Shift + Enter` or by clicking the Play button.

3. **Experimental Rigour & Output:**
   * The script automatically applies a **warm-up run** (un-timed) followed by **7 repeated timed runs**, extracting the **median execution time** to eliminate OS jitter.
   * It outputs correctness verification via independent oracles, total nodes visited, and median runtimes in milliseconds.

---

## 📊 Summary of Conflict Checking Strategies
| Strategy | Description | Complexity per Check |
| :--- | :--- | :--- |
| **Scanning** | Iterates through historical assignments dynamically. | $O(N)$ or $O(V)$ |
| **Used-marks** | Uses tracking arrays/sets for columns and diagonals. | $O(1)$ |
| **Bitmasks** | Encodes state flags into binary bits for ultra-fast bitwise logic. | $O(1)$ (Hardware-level) |
