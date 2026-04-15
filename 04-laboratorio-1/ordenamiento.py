from __future__ import annotations

import random
import statistics
import time
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt

DOCUMENTO = "1000538243"
SIZES = [10, 50, 100, 500, 1000, 5000]
REPEATS = 10

BASE_DIR = Path(__file__).resolve().parent
PLOTS_DIR = BASE_DIR / "results" / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def build_sort_array(documento: str) -> list[int]:
    digits = [int(ch) for ch in documento if ch.isdigit()]
    last_non_zero = next((d for d in reversed(digits) if d != 0), 0)
    return [last_non_zero if d == 0 else d for d in digits]


def merge(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr.copy()

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def insertion_sort(arr: list[int]) -> list[int]:
    a = arr.copy()

    for j in range(1, len(a)):
        key = a[j]
        i = j - 1

        while i >= 0 and a[i] > key:
            a[i + 1] = a[i]
            i -= 1

        a[i + 1] = key

    return a


def generate_random_array(n: int) -> list[int]:
    return [random.randint(0, 10000) for _ in range(n)]


def average_time(fn, arr: list[int], repeats: int = REPEATS) -> float:
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn(arr)
        end = time.perf_counter()
        times.append(end - start)
    return statistics.mean(times)


def benchmark() -> tuple[list[float], list[float]]:
    merge_times = []
    insertion_times = []

    for n in SIZES:
        merge_runs = []
        insertion_runs = []

        for _ in range(REPEATS):
            base = generate_random_array(n)

            start = time.perf_counter()
            merge_sort(base)
            end = time.perf_counter()
            merge_runs.append(end - start)

            start = time.perf_counter()
            insertion_sort(base)
            end = time.perf_counter()
            insertion_runs.append(end - start)

        merge_times.append(statistics.mean(merge_runs))
        insertion_times.append(statistics.mean(insertion_runs))

    return merge_times, insertion_times


def plot_results(merge_times: list[float], insertion_times: list[float]) -> None:
    plt.figure(figsize=(9, 5))
    plt.plot(SIZES, merge_times, marker="o", label="Merge Sort")
    plt.plot(SIZES, insertion_times, marker="o", label="Insertion Sort")

    plt.title("Comparación de tiempos: Merge Sort vs Insertion Sort")
    plt.xlabel("Tamaño de entrada (n)")
    plt.ylabel("Tiempo promedio (s)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    output_file = PLOTS_DIR / "ordenamiento.png"
    plt.savefig(output_file, dpi=200)
    plt.show()

    print(f"Gráfica guardada en: {output_file}")


def main() -> None:
    random.seed(42)

    arr_doc = build_sort_array(DOCUMENTO)
    print("Documento:", DOCUMENTO)
    print("Arreglo del documento para ordenamiento:", arr_doc)
    print("Merge Sort:", merge_sort(arr_doc))
    print("Insertion Sort:", insertion_sort(arr_doc))

    merge_times, insertion_times = benchmark()

    print("\nTiempos promedio:")
    for n, t1, t2 in zip(SIZES, merge_times, insertion_times):
        print(f"n={n:<5} merge sort={t1:.8f}s   insertion sort={t2:.8f}s")

    plot_results(merge_times, insertion_times)


if __name__ == "__main__":
    main()