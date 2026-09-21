# Compatibility Test Coverage Details

> Updated: 2026-06-17
> Test environment: openRuyi RISC-V (10.20.237.192:12055)
> 1 test suite (ltp_posix), 10 POSIX categories, 188 interface test cases
> Final result: 570 PASS / 36 FAIL / 20 SKIP (gcc fix + sudo verification)
> Old template tests removed; each POSIX interface is an independent test case

## Overview

| Category | Cases | PASS | FAIL | SKIP | Status |
|------|:---:|:---:|:---:|:---:|:---:|
| [pthread](#pthread) | 95 | 286 | 13 | 0 | ✅ |
| [signal](#signal) | 22 | 46 | 0 | 18 | ✅ |
| [filesystem](#filesystem) | 16 | 24 | 0 | 0 | ✅ |
| [mqueue](#mqueue) | 10 | 42 | 0 | 2 | ✅ |
| [semaphore](#semaphore) | 9 | 26 | 7 | 0 | ⚠️ |
| [sched](#sched) | 8 | 23 | 11 | 0 | ⚠️ |
| [mmap](#mmap) | 8 | 42 | 2 | 0 | ✅ |
| [aio](#aio) | 8 | 21 | 3 | 0 | ✅ |
| [clocks](#clocks) | 7 | 32 | 0 | 0 | ✅ |
| [timer](#timer) | 5 | 28 | 0 | 0 | ✅ |
| **Total** | **188** | **570** | **36** | **20** | |

> SKIP reduced to 20 via `-std=gnu11` + `-Wno-error=incompatible-pointer-types` (remaining ones are POSIX deprecated functions sighold/sigignore, etc.).

## Test Principles

This compatibility test is based on [LTP (Linux Test Project)](https://github.com/linux-test-project/ltp)'s `open_posix_testsuite`, verifying openRuyi RISC-V system compliance with the POSIX 1003.1-2001 standard.

### Test Methods

- **Shell script tests** (`.sh`): directly execute LTP test scripts
- **C source tests** (`.c`): compile on-the-fly with `gcc` (linking `lib/common.c` test framework), then execute

### Directory Structure

```
tests/compatibility/ltp_posix/
├── main.fmf                    # Test suite metadata
├── setup.sh                    # Environment setup (install deps, clone LTP)
├── teardown.sh                 # Environment cleanup
├── helper.sh                   # Common helper functions (compile + run)
├── test.sh                     # Main test script (aggregates all 188 cases)
├── pthread/                    # pthread multithreading (95 cases)
│   ├── test_ltp_posix_pthread_create/
│   ├── test_ltp_posix_pthread_mutex_init/
│   └── ...
├── signal/                     # Signals (22 cases)
│   ├── test_ltp_posix_signal_sigaction/
│   └── ...
├── filesystem/                 # Filesystem (16 cases)
├── mqueue/                     # Message queues (10 cases)
├── semaphore/                  # Semaphores (9 cases)
├── sched/                      # Scheduling (8 cases)
├── mmap/                       # Memory mapping (8 cases)
├── aio/                        # Async I/O (8 cases)
├── clocks/                     # Clocks (7 cases)
└── timer/                      # Timers (5 cases)
```

---

## Category Details

### pthread {#pthread}

95 test cases covering all pthread_* POSIX interfaces: thread create/destroy, mutex, condition variable, rwlock, barrier, spinlock, thread attributes, thread-local storage, cancellation, signal mask, etc.

### signal {#signal}

22 test cases covering signal handling interfaces: sigaction, sigprocmask, sigwait, sigqueue, sigtimedwait, sigpending, sigsuspend, kill, raise, etc.

### filesystem {#filesystem}

16 test cases covering filesystem and basic C library interfaces: access, fork, fsync, getpid, strchr, strcpy, strlen, strftime, time, asctime, etc.

### mqueue {#mqueue}

10 test cases covering POSIX message queue interfaces: mq_open, mq_close, mq_send, mq_receive, mq_notify, mq_getattr, mq_setattr, mq_timedreceive, mq_timedsend, mq_unlink.

### semaphore {#semaphore}

9 test cases covering POSIX semaphore interfaces: sem_init, sem_open, sem_close, sem_wait, sem_post, sem_timedwait, sem_getvalue, sem_destroy, sem_unlink.

### sched {#sched}

8 test cases covering scheduling interfaces: sched_get_priority_max/min, sched_getparam, sched_setparam, sched_getscheduler, sched_setscheduler, sched_yield, sched_rr_get_interval.

### mmap {#mmap}

8 test cases covering memory mapping interfaces: mmap, munmap, mlock, mlockall, munlock, munlockall, shm_open, shm_unlink.

### aio {#aio}

8 test cases covering async I/O interfaces: aio_read, aio_write, aio_error, aio_return, aio_suspend, aio_cancel, aio_fsync, lio_listio.

### clocks {#clocks}

7 test cases covering clock interfaces: clock_getres, clock_gettime, clock_settime, clock_nanosleep, clock_getcpuclockid, clock, nanosleep.

### timer {#timer}

5 test cases covering timer interfaces: timer_create, timer_delete, timer_getoverrun, timer_gettime, timer_settime.
