import time
import statistics
import json
from pathlib import Path

from geneweaver.cpu_aligner import align_sequences


def benchmark_alignment(length, repetitions=5):
    sequence = ("ATCG" * ((length + 3) // 4))[:length]
    target = sequence[:-1] + ("A" if sequence[-1] != "A" else "C")

    align_sequences(sequence, target)  # Warm-up
    timings = []

    for _ in range(repetitions):
        start = time.perf_counter()
        align_sequences(sequence, target)
        timings.append(time.perf_counter() - start)

    return {
        "sequence_length": length,
        "repetitions": repetitions,
        "average_time_ms": round(statistics.mean(timings) * 1000, 4),
        "minimum_time_ms": round(min(timings) * 1000, 4),
        "maximum_time_ms": round(max(timings) * 1000, 4)
    }


def main():
    results = []

    for length in [25, 50, 100, 200]:
        result = benchmark_alignment(length)
        results.append(result)
        print(result)

    output_path = Path("reports/cpu_benchmark.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=4), encoding="utf-8")
    print(f"\nBenchmark results saved to {output_path}")


if __name__ == "__main__":
    main()
