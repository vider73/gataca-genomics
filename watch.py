"""Live progress console for GATACA runs.

Reads runs/progress/*.json (written by gataca.Progress from every training script), the queue logs
runs/*.log and nvidia-smi, and redraws every --every seconds. Ctrl+C to quit.

    python watch.py            # live
    python watch.py --once     # one snapshot (e.g. over ssh or in a log)
"""

import argparse
import json
import subprocess
import time
from pathlib import Path

from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.table import Table
from rich.text import Text

STALE_S = 120


def fmt_time(s: float) -> str:
    s = int(max(0, s))
    return f"{s // 3600}h{s % 3600 // 60:02d}m" if s >= 3600 else f"{s // 60}m{s % 60:02d}s"


def gpu_line() -> Text:
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw",
                              "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=5).stdout.strip()
        name, util, used, total, temp, power = [x.strip() for x in out.splitlines()[0].split(",")]
        t = Text(f"{name}  ", style="bold")
        t.append(f"util {util:>3}%  ", style="green" if int(util) > 50 else "yellow")
        t.append(f"mem {int(used) / 1024:.1f}/{int(total) / 1024:.0f} GB  temp {temp}°C  {float(power):.0f} W")
        return t
    except Exception as e:  # no GPU / no nvidia-smi
        return Text(f"GPU: n/a ({e.__class__.__name__})", style="dim")


def runs_table(runs_dir: Path, show_done: int) -> Table:
    states = []
    for f in (runs_dir / "progress").glob("*.json"):
        try:
            with open(f, "rb") as fh:  # read and release immediately: the writer needs to replace the file
                states.append(json.loads(fh.read()))
        except (json.JSONDecodeError, OSError):
            continue  # being rewritten right now
    now = time.time()
    running = sorted((s for s in states if s["status"] == "running"), key=lambda s: s["started"])
    done = sorted((s for s in states if s["status"] == "done"), key=lambda s: -s["updated"])[:show_done]

    t = Table(expand=True, box=None, pad_edge=False)
    for col, kw in [("run", {"style": "bold cyan", "no_wrap": True}), ("kind", {"style": "dim"}),
                    ("progress", {"ratio": 3}), ("step", {"justify": "right"}), ("it/s", {"justify": "right"}),
                    ("elapsed", {"justify": "right"}), ("ETA", {"justify": "right"}), ("metrics", {"ratio": 3})]:
        t.add_column(col, **kw)
    for s in running + done:
        elapsed = s["updated"] - s["started"]
        rate = s["step"] / elapsed if elapsed > 0 else 0.0
        eta = (s["total"] - s["step"]) / rate if rate > 0 else 0
        stale = s["status"] == "running" and now - s["updated"] > STALE_S
        status = "done" if s["status"] == "done" else ("stalled?" if stale else "")
        bar = ProgressBar(total=s["total"], completed=s["step"], complete_style="green" if s["status"] == "done" else
                          ("red" if stale else "magenta"))
        metrics = "  ".join(f"{k} {v:.4g}" for k, v in s["metrics"].items())
        t.add_row(s["run"], s["kind"].replace("train_", ""), bar, f"{s['step']:,}/{s['total']:,}",
                  f"{rate:.1f}", fmt_time(elapsed), status or fmt_time(eta),
                  Text(metrics, style="dim" if s["status"] == "done" else ""))
    if not running and not done:
        t.add_row("—", "", Text("no runs with live progress yet", style="dim"), "", "", "", "", "")
    return t


def queue_panel(runs_dir: Path, lines: int) -> Group:
    parts = []
    for log in sorted(runs_dir.glob("*.log"), key=lambda p: -p.stat().st_mtime)[:3]:
        tail = [l.rstrip() for l in log.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()][-lines:]
        age = fmt_time(time.time() - log.stat().st_mtime)
        parts.append(Text(f"{log.name}  (updated {age} ago)", style="bold"))
        parts += [Text("  " + l[:160], style="dim") for l in tail]
    return Group(*parts) if parts else Group(Text("no queue logs", style="dim"))


def render(runs_dir: Path, show_done: int, log_lines: int):
    return Group(
        Panel(gpu_line(), title=f"GATACA  ·  {time.strftime('%H:%M:%S')}", border_style="blue"),
        Panel(runs_table(runs_dir, show_done), title="runs", border_style="magenta"),
        Panel(queue_panel(runs_dir, log_lines), title="queues (newest logs)", border_style="dim"),
    )


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--runs-dir", type=Path, default=Path("runs"))
    p.add_argument("--every", type=float, default=2.0)
    p.add_argument("--done", type=int, default=6, help="finished runs to keep on screen")
    p.add_argument("--log-lines", type=int, default=3)
    p.add_argument("--once", action="store_true")
    args = p.parse_args()

    if args.once:
        Console(width=160).print(render(args.runs_dir, args.done, args.log_lines))
        return
    with Live(render(args.runs_dir, args.done, args.log_lines), refresh_per_second=4, screen=False) as live:
        try:
            while True:
                time.sleep(args.every)
                live.update(render(args.runs_dir, args.done, args.log_lines))
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
