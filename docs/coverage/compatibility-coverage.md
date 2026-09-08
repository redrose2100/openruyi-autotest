# 兼容性测试覆盖详情

> 更新日期：2026-06-17
> 测试环境：openRuyi RISC-V（10.20.237.192:12055）
> 共 1 个测试套（ltp_posix），10 个 POSIX 分类，188 个接口测试用例
> 最终结果：570 PASS / 36 FAIL / 20 SKIP（gcc 修复 + sudo 验证）
> 旧模版测试已移除，每个 POSIX 接口独立为一个测试用例

## 一览表

| 分类 | 用例数 | PASS | FAIL | SKIP | 状态 |
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
| **合计** | **188** | **570** | **36** | **20** | |

> SKIP 已通过 `-std=gnu11` + `-Wno-error=incompatible-pointer-types` 修复至 20（剩余为 POSIX 废弃函数 sighold/sigignore 等）。

## 测试原理

本兼容性测试基于 [LTP (Linux Test Project)](https://github.com/linux-test-project/ltp) 的 `open_posix_testsuite`，验证 openRuyi RISC-V 系统对 POSIX 1003.1-2001 标准的兼容性。

### 测试方式

- **Shell 脚本测试** (`.sh`)：直接执行 LTP 中的测试脚本
- **C 源码测试** (`.c`)：使用 `gcc` 现场编译（链接 `lib/common.c` 测试框架）后执行

### 目录结构

```
tests/compatibility/ltp_posix/
├── main.fmf                    # 测试套件元数据
├── setup.sh                    # 环境准备（安装依赖、clone LTP）
├── teardown.sh                 # 环境清理
├── helper.sh                   # 公共辅助函数（编译+运行）
├── test.sh                     # 主测试脚本（聚合全部 188 个用例）
├── pthread/                    # pthread 多线程（95 个用例）
│   ├── test_ltp_posix_pthread_create/
│   ├── test_ltp_posix_pthread_mutex_init/
│   └── ...
├── signal/                     # 信号（22 个用例）
│   ├── test_ltp_posix_signal_sigaction/
│   └── ...
├── filesystem/                 # 文件系统（16 个用例）
├── mqueue/                     # 消息队列（10 个用例）
├── semaphore/                  # 信号量（9 个用例）
├── sched/                      # 调度（8 个用例）
├── mmap/                       # 内存映射（8 个用例）
├── aio/                        # 异步 I/O（8 个用例）
├── clocks/                     # 时钟（7 个用例）
└── timer/                      # 定时器（5 个用例）
```

---

## 分类详情

### pthread {#pthread}

95 个测试用例，覆盖全部 pthread_* POSIX 接口：线程创建/销毁、互斥锁、条件变量、读写锁、屏障、自旋锁、线程属性、线程局部存储、取消、信号掩码等。

### signal {#signal}

22 个测试用例，覆盖信号处理接口：sigaction、sigprocmask、sigwait、sigqueue、sigtimedwait、sigpending、sigsuspend、kill、raise 等。

### filesystem {#filesystem}

16 个测试用例，覆盖文件系统及基础 C 库接口：access、fork、fsync、getpid、strchr、strcpy、strlen、strftime、time、asctime 等。

### mqueue {#mqueue}

10 个测试用例，覆盖 POSIX 消息队列接口：mq_open、mq_close、mq_send、mq_receive、mq_notify、mq_getattr、mq_setattr、mq_timedreceive、mq_timedsend、mq_unlink。

### semaphore {#semaphore}

9 个测试用例，覆盖 POSIX 信号量接口：sem_init、sem_open、sem_close、sem_wait、sem_post、sem_timedwait、sem_getvalue、sem_destroy、sem_unlink。

### sched {#sched}

8 个测试用例，覆盖调度接口：sched_get_priority_max/min、sched_getparam、sched_setparam、sched_getscheduler、sched_setscheduler、sched_yield、sched_rr_get_interval。

### mmap {#mmap}

8 个测试用例，覆盖内存映射接口：mmap、munmap、mlock、mlockall、munlock、munlockall、shm_open、shm_unlink。

### aio {#aio}

8 个测试用例，覆盖异步 I/O 接口：aio_read、aio_write、aio_error、aio_return、aio_suspend、aio_cancel、aio_fsync、lio_listio。

### clocks {#clocks}

7 个测试用例，覆盖时钟接口：clock_getres、clock_gettime、clock_settime、clock_nanosleep、clock_getcpuclockid、clock、nanosleep。

### timer {#timer}

5 个测试用例，覆盖定时器接口：timer_create、timer_delete、timer_getoverrun、timer_gettime、timer_settime。
