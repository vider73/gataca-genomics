"""Exit 0 when no GPU job is running, 1 otherwise (for queue scripts: one GPU task at a time).

Files named pod_*.json are remote jobs (RunPod) and are skipped. A job counts as running when its
runs/progress/<run>.json says "running" and its process is still alive, however long since its last update
(a slow evaluation may report only every half hour).
The 4090 is shared with the sister project (tokenizers, ../GaTaCa), so its runs/progress is checked too.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def alive(pid: int) -> bool:
    if os.name == "nt":
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout
        return str(pid) in out
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def running_jobs(progress_dir: Path) -> list[str]:
    jobs = []
    for f in progress_dir.glob("*.json"):
        if f.name.startswith("pod_"):
            continue
        try:
            d = json.loads(f.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if d.get("status") == "running" and alive(int(d.get("pid", -1))):
            jobs.append(d["run"])
    return jobs


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--progress-dir", type=Path, nargs="+",
                   default=[Path("runs/progress"), Path("../GaTaCa/runs/progress")],
                   help="progress folders of every project that uses this GPU (missing ones are skipped)")
    p.add_argument("--ignore", nargs="*", default=[], help="runs that do not use the local GPU (e.g. remote pods)")
    args = p.parse_args()
    jobs = [j for d in args.progress_dir if d.is_dir() for j in running_jobs(d) if j not in args.ignore]
    print("busy: " + ", ".join(jobs) if jobs else "idle")
    sys.exit(1 if jobs else 0)


if __name__ == "__main__":
    main()
