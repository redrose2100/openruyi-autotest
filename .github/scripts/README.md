# CI CLI (.github/scripts)

A unified **class-based CLI framework** that encapsulates everything needed by CI pipelines as reusable commands.
Pipelines (workflows) only invoke the CLI; all implementation logic lives inside the `scripts` directory for easy extension and maintenance.

## Quick Start

```bash
# List all registered commands
python3 .github/scripts/cli.py --help

# Show a command's parameters
python3 .github/scripts/cli.py compute-requirements --help

# Execute a command (-v for INFO, -vv for DEBUG, optionally --log-file)
python3 .github/scripts/cli.py -v compute-requirements \
  --repo . --changed-files changed.txt --output req.json
```

> All commands share two global parameters: `--verbose/-v` (repeatable, 0=WARNING / 1=INFO / 2=DEBUG) and `--log-file`.

## Architecture

```
.github/scripts/
├── cli.py                     # Entry point: parses global args, delegates to core.base.main()
├── __main__.py                # Supports python3 -m scripts
├── core/                      # Shared library (base classes + infrastructure)
│   ├── base.py                #   BaseCommand + CommandRegistry + argument parsing
│   ├── logging.py             #   Unified logging (console + optional JSON log file)
│   ├── config.py              #   Environment variables / JSON / GitHub Actions output tools
│   ├── ssh.py                 #   Unified SSH client (ExecResult / SSHClient / wait_ssh_ready)
│   ├── cloudpods.py           #   CloudPods API client (create/query/delete servers)
│   ├── github.py              #   GitHub REST API wrapper (PR comments etc.)
│   └── repo.py                #   Repo root detection, packaging, changed file collection
└── commands/                  # Command implementations: one file per CI step, auto-registered
    ├── compute_requirements.py
    ├── launch_qemu_env.py
    ├── run_tests_in_qemu.py
    ├── post_pr_comment.py
    └── cleanup_cloudpods.py
```

## Design Highlights

- **Auto-registration**: `CommandRegistry.discover()` scans `commands/*.py`; any class inheriting `BaseCommand`
  and defined in the scanned file is automatically registered as a subcommand — no registration code changes needed.
- **Object-oriented**: One command per file; commands communicate only through JSON artifacts (`requirements.json`,
  `vm_info.json`, `test_results.json`), making them independently replaceable/extensible.
- **Lifecycle**: `on_start → run → on_finish`, all exceptions are unified (`KeyboardInterrupt → 130`,
  everything else `→ 1`, with traceback printed under `-vv`).
- **Unified config**: Commands read configuration via environment variables or JSON; credentials are never
  committed to the repo (injected via `secrets.*` in GitHub Actions).

## Extension Guide: Adding a New Command

Create a new file under `commands/`, e.g. `commands/hello.py`:

```python
from core.base import BaseCommand


class HelloWorldCommand(BaseCommand):
    name = "hello-world"
    description = "Print a greeting"

    def setup_parser(self, parser):
        parser.add_argument("--who", default="world", help="Who to greet")

    def run(self, args):
        self.log_info("Hello, %s!", args.who)
        return 0
```

Takes effect immediately after saving — no registration required:

```bash
python3 .github/scripts/cli.py hello-world --who ci
```

## Command Reference

| Command | Purpose | Key Input | Output |
| --- | --- | --- | --- |
| `compute-requirements` | Compute resource specs (CPU/memory/SKU/dependencies) from changed test files | `--changed-files` | `requirements.json` |
| `launch-qemu-env` | Create a RISC-V QEMU environment via CloudPods and wait for readiness | `requirements.json` | `vm_info.json` |
| `run-tests-in-qemu` | Execute tmt/BeakerLib tests remotely via SSH and aggregate results | `vm_info.json` | `test_results.json` |
| `post-pr-comment` | Publish test results as a Markdown comment on the PR | `test_results.json` | PR comment |
| `cleanup-cloudpods` | Destroy CloudPods servers created in this run to avoid lingering charges | `vm_info.json` | — |

## Pipeline Integration

Execution order in `pr-tests-changed.yml` (each step is a single CLI invocation):

```yaml
python3 .github/scripts/cli.py compute-requirements ...   # 1. Compute resource specs
python3 .github/scripts/cli.py launch-qemu-env ...          # 2. Spin up QEMU env
python3 .github/scripts/cli.py run-tests-in-qemu ...        # 3. Execute tests
python3 .github/scripts/cli.py cleanup-cloudpods ...        # 4. Clean up env
```

> Note: The pipeline no longer auto-publishes PR comments (PRs from fork repos have
> read-only `GITHUB_TOKEN`, causing the comment API to return 403). The `post-pr-comment`
> command is kept for same-repo PRs or manual scenarios.

## Testing

`unittests/test_ci_cli.py` covers: command auto-discovery, base class conventions,
`compute-requirements` spec calculation, PR comment Markdown generation, etc.
Run locally:

```bash
python -m pytest unittests/test_ci_cli.py -q
```
