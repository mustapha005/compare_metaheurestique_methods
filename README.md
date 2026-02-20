# TSP Metaheuristics Solver

## Project Structure

```
project/
├── algo.py
├── exemple.py
├── data/
│   ├── eil51.tsp
│   ├── ulysses22.tsp
│   └── st70.tsp
└── resultat/
```

## Dataset

Download `.tsp` files manually from [TSPLIB on GitHub](https://github.com/mastqe/tsplib) and place them in the `data/` folder.

## Installation

```bash
pip install -m requerement.txt
```

## Usage

```bash
python exemple.py
```

After running, the `resultat/` folder will contain:

- `tsp_benchmark_results.csv` — all results (algorithm, cost, time, tested, explored) for each instance
- `chapter1_cost_*.png` — bar charts comparing solution cost per instance
- `chapter2_time_*.png` — bar charts comparing execution time per instance
- `chapter3_tested_*.png` — bar charts comparing tested edges per instance
- `chapter4_explored_*.png` — bar charts comparing explored edges per instance
