# UnixBench Performance Test Results

> Test server: 10.20.237.192:12055
> Test time: 2026-06-22

## Test Case Execution Results

| Test Case | Exit Code | Composite Score |
|-----------|-----------|-----------------|
| test_unixbench_single_thread | 0 | System Benchmarks Index Score 25.8 |
| test_unixbench_multi_thread | 0 | System Benchmarks Index Score 85.7 |
| test_unixbench_integer_only | 0 | System Benchmarks Index Score (Partial Only)                           61.1 |
| test_unixbench_io_only | 0 | System Benchmarks Index Score (Partial Only)                           55.0 |
| test_unixbench_process_only | 0 | System Benchmarks Index Score (Partial Only)                            9.4 |
| test_unixbench_quick_mode | 0 | System Benchmarks Index Score (Partial Only)                           20.2 |
| test_unixbench_half_cpu | 0 | System Benchmarks Index Score                                          85.8 |

## Conclusion
- Single-thread composite score: **25.8**
- Multi-thread composite score: **85.7** (parallel speedup ~3.3x)
- Server successfully executed UnixBench benchmark tests
