from __future__ import annotations

import random
import statistics
import time
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt

DOCUMENTO = "1000538243"
SIZES = [10, 50, 100, 200, 500, 1000]
REPEATS = 10

BASE_DIR = Path(__file__).resolve().parent
PLOTS_DIR = BASE_DIR / "results" / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def build_arrays(documento: str) -> tuple[list[int], list[int]]:
    digits = [int(ch) for ch in documento if ch.isdigit()]

    last_non_zero = next((d for d in reversed(digits) if d != 0), 0)
    normalized = [last_non_zero if d == 0 else d for d in digits]

    array_subarray = [value if i % 2 == 0 else -value for i, value in enumerate(normalized)]
    array_sorting = normalized.copy()

    return array_subarray, array_sorting


def max_subarray_bruteforce(arr: list[int]) -> tuple[int, int, int]:
    if not arr:
        raise ValueError("El arreglo no puede estar vacío.")

    max_sum = float("-inf")
    start = end = 0

    for i in range(len(arr)):
        current_sum = 0
        for j in range(i, len(arr)):
            current_sum += arr[j]
            if current_sum > max_sum:
                max_sum = current_sum
                start = i
                end = j

    return start, end, int(max_sum)


def max_crossing_subarray(arr: list[int], low: int, mid: int, high: int) -> tuple[int, int, int]:
    left_sum = float("-inf")
    total = 0
    max_left = mid

    for i in range(mid, low - 1, -1):
        total += arr[i]
        if total > left_sum:
            left_sum = total
            max_left = i

    right_sum = float("-inf")
    total = 0
    max_right = mid + 1

    for j in range(mid + 1, high + 1):
        total += arr[j]
        if total > right_sum:
            right_sum = total
            max_right = j

    return max_left, max_right, int(left_sum + right_sum)


def max_subarray_divide_and_conquer(arr: list[int], low: int = 0, high: int | None = None) -> tuple[int, int, int]:
    if not arr:
        raise ValueError("El arreglo no puede estar vacío.")

    if high is None:
        high = len(arr) - 1

    if low == high:
        return low, high, arr[low]

    mid = (low + high) // 2

    left_low, left_high, left_sum = max_subarray_divide_and_conquer(arr, low, mid)
    right_low, right_high, right_sum = max_subarray_divide_and_conquer(arr, mid + 1, high)
    cross_low, cross_high, cross_sum = max_crossing_subarray(arr, low, mid, high)

    if left_sum >= right_sum and left_sum >= cross_sum:
        return left_low, left_high, left_sum
    elif right_sum >= left_sum and right_sum >= cross_sum:
        return right_low, right_high, right_sum
    else:
        return cross_low, cross_high, cross_sum


def generate_random_array(n: int) -> list[int]:
    return [random.randint(-100, 100) for _ in range(n)]


def average_time(fn, arr: list[int], repeats: int = REPEATS) -> float:
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn(arr)
        end = time.perf_counter()
        times.append(end - start)
    return statistics.mean(times)


def benchmark() -> tuple[list[float], list[float]]:
    brute_times = []
    dac_times = []

    for n in SIZES:
        arr = generate_random_array(n)

        brute_times.append(average_time(max_subarray_bruteforce, arr))
        dac_times.append(average_time(max_subarray_divide_and_conquer, arr))

    return brute_times, dac_times


def plot_results(brute_times: list[float], dac_times: list[float]) -> None:
    plt.figure(figsize=(9, 5))
    plt.plot(SIZES, brute_times, marker="o", label="Fuerza bruta")
    plt.plot(SIZES, dac_times, marker="o", label="Divide y vencerás")

    plt.title("Comparación de tiempos: Subarreglo máximo")
    plt.xlabel("Tamaño de entrada (n)")
    plt.ylabel("Tiempo promedio (s)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    output_file = PLOTS_DIR / "subarreglo_maximo.png"
    plt.savefig(output_file, dpi=200)
    plt.show()

    print(f"Gráfica guardada en: {output_file}")


def main() -> None:
    random.seed(42)

    arr_subarray, arr_sorting = build_arrays(DOCUMENTO)

    print("Documento:", DOCUMENTO)
    print("Arreglo para subarreglo máximo:", arr_subarray)
    print("Arreglo para ordenamiento:", arr_sorting)

    b_low, b_high, b_sum = max_subarray_bruteforce(arr_subarray)
    d_low, d_high, d_sum = max_subarray_divide_and_conquer(arr_subarray)

    print("\nResultado fuerza bruta:")
    print(f"Inicio: {b_low}, Fin: {b_high}, Suma: {b_sum}")
    print("Subarreglo:", arr_subarray[b_low:b_high + 1])

    print("\nResultado divide y vencerás:")
    print(f"Inicio: {d_low}, Fin: {d_high}, Suma: {d_sum}")
    print("Subarreglo:", arr_subarray[d_low:d_high + 1])

    brute_times, dac_times = benchmark()

    print("\nTiempos promedio:")
    for n, t1, t2 in zip(SIZES, brute_times, dac_times):
        print(f"n={n:<5} fuerza bruta={t1:.8f}s   divide y vencerás={t2:.8f}s")

    plot_results(brute_times, dac_times)


if __name__ == "__main__":
    main()