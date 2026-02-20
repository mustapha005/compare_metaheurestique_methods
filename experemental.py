import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from algo import (
    load_tsp_to_matrix,
    swap, two_opt,
    hill_climbing_best,
    hill_climbing_first,
    multi_start_hill_climbing,
    simulated_annealing,
    tabu_search,
)

os.makedirs("resultat", exist_ok=True)


class TSPReport:
    def __init__(self):
        self.results = []

    def measure_time(self, func, *args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        return result, elapsed

    def run_benchmarks(self, solver_dict):
        algorithms = [
            ("HC Best (Swap)",             lambda dm: hill_climbing_best(dm, swap, max_iter=1000)),
            ("HC Best (Two-Opt)",          lambda dm: hill_climbing_best(dm, two_opt, max_iter=1000)),
            ("HC First (Swap)",            lambda dm: hill_climbing_first(dm, swap, max_iter=1000)),
            ("HC First (Two-Opt)",         lambda dm: hill_climbing_first(dm, two_opt, max_iter=1000)),
            ("Multi-Start HC (Swap)",      lambda dm: multi_start_hill_climbing(dm, swap, hill_climbing_best, num_restarts=10, max_iter=1000)),
            ("Multi-Start HC (Two-Opt)",   lambda dm: multi_start_hill_climbing(dm, two_opt, hill_climbing_best, num_restarts=10, max_iter=1000)),
            ("Simulated Annealing (Swap)", lambda dm: simulated_annealing(dm, swap, max_iter=1000, initial_temp=1000)),
            ("Simulated Annealing (Two-Opt)", lambda dm: simulated_annealing(dm, two_opt, max_iter=1000, initial_temp=1000)),
            ("Tabu Search (Swap)",         lambda dm: tabu_search(dm, swap, max_iter=1000, tabu_size=10)),
            ("Tabu Search (Two-Opt)",      lambda dm: tabu_search(dm, two_opt, max_iter=1000, tabu_size=10)),
        ]

        for file_name, distance_matrix in solver_dict.items():
            print(f"\nBenchmarking {file_name}...")
            for algo_name, algo_func in algorithms:
                (solution, cost, tested, explored), exec_time = self.measure_time(algo_func, distance_matrix)
                self.results.append({
                    "File": file_name,
                    "Algorithm": algo_name,
                    "Cost": cost,
                    "Time (s)": round(exec_time, 4),
                    "Tested": tested,
                    "Explored": explored,
                })

    def get_dataframe(self):
        return pd.DataFrame(self.results)

    def _print_table(self, df, title=None):
        if title:
            print(f"\n  {title}")
        col_widths = {col: max(len(col), df[col].astype(str).map(len).max()) for col in df.columns}
        sep = "+" + "+".join("-" * (w + 2) for w in col_widths.values()) + "+"
        header = "|" + "|".join(f" {col:<{col_widths[col]}} " for col in df.columns) + "|"
        print(sep)
        print(header)
        print(sep.replace("-", "="))
        for _, row in df.iterrows():
            print("|" + "|".join(f" {str(row[col]):<{col_widths[col]}} " for col in df.columns) + "|")
        print(sep)

    def _print_stats(self, df, metric, label):
        stats = (
            df.groupby("Algorithm")[metric]
            .agg(Min="min", Max="max", Mean="mean", Std="std")
            .round(2)
            .reset_index()
        )
        self._print_table(stats, title=f"Statistics — {label} (across all files)")

    def chapter1_cost(self, df):
        print("\n" + "=" * 60)
        print("CHAPTER 1: SOLUTION COST (Lower is Better)")
        print("=" * 60)
        for file_name in df["File"].unique():
            file_data = df[df["File"] == file_name].sort_values("Cost").reset_index(drop=True)
            self._print_table(file_data[["Algorithm", "Cost"]], title=f"File: {file_name}")
            plt.figure(figsize=(14, 10))
            sns.barplot(data=file_data, x="Cost", y="Algorithm", hue="Algorithm", palette="RdYlGn_r", legend=False)
            plt.title(f"Solution Cost - {file_name}\n(Lower is Better)", fontsize=16, fontweight="bold", pad=20)
            plt.xlabel("Cost", fontsize=14, fontweight="bold")
            plt.ylabel("Algorithm", fontsize=14, fontweight="bold")
            plt.tight_layout()
            plt.savefig(f"resultat/chapter1_cost_{file_name.replace('.tsp', '')}.png", dpi=300, bbox_inches="tight")
            plt.close()
        self._print_stats(df, "Cost", "Solution Cost")

    def chapter2_time(self, df):
        print("\n" + "=" * 60)
        print("CHAPTER 2: EXECUTION TIME (Lower is Better)")
        print("=" * 60)
        for file_name in df["File"].unique():
            file_data = df[df["File"] == file_name].sort_values("Time (s)").reset_index(drop=True)
            self._print_table(file_data[["Algorithm", "Time (s)"]], title=f"File: {file_name}")
            plt.figure(figsize=(12, 8))
            sns.barplot(data=file_data, x="Time (s)", y="Algorithm", hue="Algorithm", palette="Blues_r", legend=False)
            plt.title(f"Execution Time - {file_name}\n(Lower is Better)", fontsize=14, fontweight="bold")
            plt.xlabel("Time (seconds)", fontsize=12)
            plt.tight_layout()
            plt.savefig(f"resultat/chapter2_time_{file_name.replace('.tsp', '')}.png", dpi=300)
            plt.close()
        self._print_stats(df, "Time (s)", "Execution Time (s)")

    def chapter3_tested(self, df):
        print("\n" + "=" * 60)
        print("CHAPTER 3: TESTED EDGES (Higher is More Thorough)")
        print("=" * 60)
        for file_name in df["File"].unique():
            file_data = df[df["File"] == file_name].sort_values("Tested", ascending=False).reset_index(drop=True)
            self._print_table(file_data[["Algorithm", "Tested"]], title=f"File: {file_name}")
            plt.figure(figsize=(12, 8))
            sns.barplot(data=file_data, x="Tested", y="Algorithm", hue="Algorithm", palette="Greens_r", legend=False)
            plt.title(f"Tested Edges - {file_name}", fontsize=14, fontweight="bold")
            plt.xlabel("Tested Edges", fontsize=12)
            plt.tight_layout()
            plt.savefig(f"resultat/chapter3_tested_{file_name.replace('.tsp', '')}.png", dpi=300)
            plt.close()
        self._print_stats(df, "Tested", "Tested Edges")

    def chapter4_explored(self, df):
        print("\n" + "=" * 60)
        print("CHAPTER 4: EXPLORED EDGES (Higher is More Exploration)")
        print("=" * 60)
        for file_name in df["File"].unique():
            file_data = df[df["File"] == file_name].sort_values("Explored", ascending=False).reset_index(drop=True)
            self._print_table(file_data[["Algorithm", "Explored"]], title=f"File: {file_name}")
            plt.figure(figsize=(12, 8))
            sns.barplot(data=file_data, x="Explored", y="Algorithm", hue="Algorithm", palette="Purples_r", legend=False)
            plt.title(f"Explored Edges - {file_name}", fontsize=14, fontweight="bold")
            plt.xlabel("Explored Edges", fontsize=12)
            plt.tight_layout()
            plt.savefig(f"resultat/chapter4_explored_{file_name.replace('.tsp', '')}.png", dpi=300)
            plt.close()
        self._print_stats(df, "Explored", "Explored Edges")

    def print_full_summary(self, df):
        print("\n" + "=" * 60)
        print("FULL RESULTS SUMMARY")
        print("=" * 60)
        for file_name in df["File"].unique():
            file_data = df[df["File"] == file_name][["Algorithm", "Cost", "Time (s)", "Tested", "Explored"]].reset_index(drop=True)
            self._print_table(file_data, title=f"File: {file_name}")


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Starting TSP Report Generation...")

    solver_dict = {
        "eil51.tsp":    load_tsp_to_matrix("data/eil51.tsp"),
        "ulysses22.tsp": load_tsp_to_matrix("data/ulysses22.tsp"),
        "st70.tsp":     load_tsp_to_matrix("data/st70.tsp"),
    }

    report = TSPReport()
    report.run_benchmarks(solver_dict)
    df = report.get_dataframe()

    report.print_full_summary(df)
    report.chapter1_cost(df)
    report.chapter2_time(df)
    report.chapter3_tested(df)
    report.chapter4_explored(df)

    df.to_csv("resultat/tsp_benchmark_results.csv", index=False)
    print("\n✓ Data saved: resultat/tsp_benchmark_results.csv")
    print("\n" + "=" * 60)
    print("✓ REPORT GENERATION COMPLETE")
    print("=" * 60)