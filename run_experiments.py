import time
import numpy as np
import matplotlib.pyplot as plt
import random
import sys
import argparse

sys.setrecursionlimit(100000)

# ==========================================
# Part A – Sorting Algorithm Implementations
# ==========================================

def bubble_sort(arr_in):
    arr = arr_in.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def selection_sort(arr_in):
    arr = arr_in.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(arr_in):
    arr = arr_in.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged += left[i:]
    merged += right[j:]
    return merged

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Algorithm registry
ALL_ALGORITHMS = {
    1: ("Bubble Sort",    bubble_sort),
    2: ("Selection Sort", selection_sort),
    3: ("Insertion Sort", insertion_sort),
    4: ("Merge Sort",     merge_sort),
    5: ("Quick Sort",     quick_sort),
}

# ==========================================
# Helper functions
# ==========================================

def generate_random_array(size):
    return np.random.randint(0, 10000, size).tolist()

def generate_nearly_sorted(size, noise_pct):
    arr = list(range(size))
    num_swaps = int(size * noise_pct)
    for _ in range(num_swaps):
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def measure(func, arr, repetitions):
    times = []
    for _ in range(repetitions):
        data = arr[:] if isinstance(arr, list) else list(arr)
        start = time.perf_counter()
        func(data)
        times.append(time.perf_counter() - start)
    return float(np.mean(times)), float(np.std(times))

def run_experiment(algorithms, sizes, repetitions, array_gen):
    results = {name: {"means": [], "stds": []} for name, _ in algorithms}
    for size in sizes:
        print(f"  size={size} ...", flush=True)
        arr = array_gen(size)
        for name, func in algorithms:
            mean, std = measure(func, arr, repetitions)
            results[name]["means"].append(mean)
            results[name]["stds"].append(std)
    return results

def plot_results(results, sizes, title, filename):
    plt.figure(figsize=(10, 6))
    for name, data in results.items():
        means = np.array(data["means"])
        stds = np.array(data["stds"])
        plt.plot(sizes, means, label=name, marker='o')
        plt.fill_between(sizes, means - stds, means + stds, alpha=0.2)
    plt.xlabel("Array size (n)")
    plt.ylabel("Runtime (seconds)")
    plt.title(title)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(filename)
    print(f"  Saved: {filename}")
    plt.show()

# ==========================================
# Part D – Command Line Interface
# ==========================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Sorting Algorithm Runtime Comparison",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-a", "--algorithms",
        nargs="+", type=int, default=[3, 4, 5],
        metavar="ID",
        help=(
            "Algorithm IDs to compare (default: 3 4 5):\n"
            "  1 = Bubble Sort\n"
            "  2 = Selection Sort\n"
            "  3 = Insertion Sort\n"
            "  4 = Merge Sort\n"
            "  5 = Quick Sort"
        ),
    )
    parser.add_argument(
        "-s", "--sizes",
        nargs="+", type=int, default=[100, 500, 1000, 2000, 3000],
        metavar="N",
        help="Array sizes to test (default: 100 500 1000 2000 3000)",
    )
    parser.add_argument(
        "-e", "--experiment",
        type=int, choices=[1, 2], default=None,
        metavar="TYPE",
        help=(
            "Experiment type for nearly sorted arrays:\n"
            "  1 = 5%% noise\n"
            "  2 = 20%% noise\n"
            "(omit to run both Part B and Part C)"
        ),
    )
    parser.add_argument(
        "-r", "--repetitions",
        type=int, default=5,
        metavar="R",
        help="Number of repetitions per measurement (default: 5)",
    )
    return parser.parse_args()

# ==========================================
# Main
# ==========================================

def main():
    args = parse_args()

    # Validate algorithm IDs
    for aid in args.algorithms:
        if aid not in ALL_ALGORITHMS:
            print(f"Error: unknown algorithm ID {aid}. Choose from 1-5.")
            sys.exit(1)

    selected = [(ALL_ALGORITHMS[aid][0], ALL_ALGORITHMS[aid][1]) for aid in args.algorithms]
    sizes = sorted(args.sizes)
    reps = args.repetitions

    print(f"Algorithms : {[name for name, _ in selected]}")
    print(f"Sizes      : {sizes}")
    print(f"Repetitions: {reps}")

    if args.experiment is None:
        # Default: run Part B (random) → result1.png  AND  Part C (5% noise) → result2.png
        print("\n[Part B] Random arrays...")
        r1 = run_experiment(selected, sizes, reps, generate_random_array)
        plot_results(r1, sizes, "Runtime Comparison (Random Arrays)", "result1.png")

        print("\n[Part C] Nearly sorted arrays (5% noise)...")
        r2 = run_experiment(selected, sizes, reps, lambda n: generate_nearly_sorted(n, 0.05))
        plot_results(r2, sizes, "Runtime Comparison (Nearly Sorted, noise=5%)", "result2.png")

    elif args.experiment == 1:
        print("\nExperiment: nearly sorted arrays (5% noise)...")
        r = run_experiment(selected, sizes, reps, lambda n: generate_nearly_sorted(n, 0.05))
        plot_results(r, sizes, "Runtime Comparison (Nearly Sorted, noise=5%)", "result2.png")

    elif args.experiment == 2:
        print("\nExperiment: nearly sorted arrays (20% noise)...")
        r = run_experiment(selected, sizes, reps, lambda n: generate_nearly_sorted(n, 0.20))
        plot_results(r, sizes, "Runtime Comparison (Nearly Sorted, noise=20%)", "result2.png")

    print("\nDone.")

if __name__ == "__main__":
    main()
