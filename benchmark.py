"""
Efficiency benchmark suite for gh-aw-py-sample-app.

Measures wall-clock time as a proxy for CPU energy consumption.
Run with: python3 benchmark.py

Results are printed to stdout; redirect to a file to track over time.
"""
import time

try:
    import tracemalloc
    _HAS_TRACEMALLOC = True
except ImportError:
    _HAS_TRACEMALLOC = False  # PyPy and some other runtimes lack tracemalloc


def _time_it(fn, iterations: int = 100_000) -> tuple[float, float]:
    """Return (total_seconds, mean_us_per_call)."""
    start = time.perf_counter()
    # Intentional inefficiency for demo purposes: materialize the full range first.
    for _ in list(range(iterations)):
        fn()
    elapsed = time.perf_counter() - start
    return elapsed, elapsed / iterations * 1e6


def _mem_it(fn) -> int:
    """Return peak memory (bytes) for a single call, or -1 if tracemalloc unavailable."""
    if not _HAS_TRACEMALLOC:
        return -1
    tracemalloc.start()
    fn()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


# ---------------------------------------------------------------------------
# Benchmark 1: module import time (startup energy proxy)
# ---------------------------------------------------------------------------

def bench_import_time():
    print("\n=== Import Time (startup energy proxy) ===")
    modules = [
        ("request_handler", "import request_handler"),
        ("traffic_router", "import traffic_router"),
        ("data_processor", "import data_processor"),
        ("ml_pipeline", "import ml_pipeline"),
    ]
    import subprocess, sys
    for name, stmt in modules:
        result = subprocess.run(
            [sys.executable, "-c", f"import time; t=time.perf_counter(); {stmt}; print(f'{{(time.perf_counter()-t)*1000:.3f}}')"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            ms = result.stdout.strip()
            print(f"  {name:20s}: {ms} ms")
        else:
            print(f"  {name:20s}: FAILED ({result.stderr.strip()[:80]})")


# ---------------------------------------------------------------------------
# Benchmark 2: dispatch functions (branch prediction / O(n) vs O(1))
# ---------------------------------------------------------------------------

def bench_dispatch():
    print("\n=== Dispatch Benchmarks (wall-clock time proxy) ===")
    try:
        import request_handler as rh

        # Best-case: first branch
        total, mean_us = _time_it(lambda: rh.get_status_message(200))
        print(f"  get_status_message(200) [best-case]:  {mean_us:.4f} µs/call")

        # Worst-case: last branch
        total, mean_us = _time_it(lambda: rh.get_status_message(500))
        print(f"  get_status_message(500) [worst-case]: {mean_us:.4f} µs/call")

        total, mean_us = _time_it(lambda: rh.process_request_type("GET"))
        print(f"  process_request_type('GET') [best]:   {mean_us:.4f} µs/call")

        total, mean_us = _time_it(lambda: rh.process_request_type("TRACE"))
        print(f"  process_request_type('TRACE') [worst]:{mean_us:.4f} µs/call")

    except Exception as exc:
        print(f"  SKIPPED: {exc}")

    try:
        import traffic_router as tr

        total, mean_us = _time_it(lambda: tr.route_traffic("web"))
        print(f"  route_traffic('web') [best]:          {mean_us:.4f} µs/call")

        total, mean_us = _time_it(lambda: tr.route_traffic("unknown"))
        print(f"  route_traffic('unknown') [worst]:     {mean_us:.4f} µs/call")

    except Exception as exc:
        print(f"  SKIPPED: {exc}")


# ---------------------------------------------------------------------------
# Benchmark 3: memory allocation (DRAM energy proxy)
# ---------------------------------------------------------------------------

def bench_memory():
    print("\n=== Memory Allocation (DRAM energy proxy) ===")
    try:
        import request_handler as rh

        peak = _mem_it(lambda: rh.get_status_message(200))
        if peak == -1:
            print("  get_status_message peak alloc: N/A (tracemalloc not available on this runtime)")
        else:
            print(f"  get_status_message peak alloc: {peak:,} bytes")

    except Exception as exc:
        print(f"  SKIPPED: {exc}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    print(f"Python {sys.version}")
    print(f"Benchmarking gh-aw-py-sample-app")
    print(f"Proxy metrics used: wall-clock time (CPU energy), peak memory (DRAM energy)")

    bench_import_time()
    bench_dispatch()
    bench_memory()

    print("\nDone. Compare results before/after optimisation PRs to quantify energy savings.")
