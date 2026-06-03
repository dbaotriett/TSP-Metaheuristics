import time
import statistics
from utils.data_loader import readTspEuc2d
from algorithms.tabu_search import tabuSearch
from algorithms.simulated_annealing import simulatedAnnealing
from algorithms.guided_local_search import guidedLocalSearch


def run_experiment(filepath, optimal_cost, num_runs=10):
    """
    Chạy thực nghiệm trên một instance và in bảng thống kê.
    """
    dist, n = readTspEuc2d(filepath)
    print(f"\nInstance: {filepath} ({n} TP), Optimal cost = {optimal_cost} ")
    print(f"{'Algo':<6}{'Best':>8}{'Avg':>10}{'Std':>10}{'Time(s)':>10}{'Gap(%)':>10}")
    print("-" * 60)

    results = {}
    for algo_name, algo_func in [("TS", tabuSearch),
                                  ("SA", simulatedAnnealing),
                                  ("GLS", guidedLocalSearch)]:
        costs = []
        times = []
        for _ in range(num_runs):
            start = time.time()
            _, cost = algo_func(dist)
            elapsed = time.time() - start
            costs.append(cost)
            times.append(elapsed)

        best = min(costs)
        avg = statistics.mean(costs)
        std = statistics.stdev(costs) if num_runs > 1 else 0.0
        avg_time = statistics.mean(times)
        gap = (best - optimal_cost) / optimal_cost * 100 if optimal_cost else 0.0

        print(f"{algo_name:<6}{best:>8}{avg:>10.1f}{std:>10.1f}{avg_time:>10.2f}{gap:>10.2f}")
        results[algo_name] = {
            "best": best, "avg": avg, "std": std,
            "avg_time": avg_time, "gap": gap
        }
    return results


if __name__ == "__main__":
    # Danh sách instance (tên file và chi phí tối ưu đã biết)
    instances = [
        ("data/eil51.tsp", 426),
        ("data/st70.tsp", 675),
        ("data/kroA100.tsp", 21282),
        ("data/pr144.tsp", 58537),
        ("data/d198.tsp", 15780),
        ("data/lin318.tsp", 42029),
        
    ]
    NUM_RUNS = 5 

    for path, opt in instances:
        try:
            run_experiment(path, opt, NUM_RUNS)
        except FileNotFoundError:
            print(f"File {path} not found.")

    