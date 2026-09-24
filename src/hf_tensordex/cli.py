"""`hf tensordex ...` — the same verbs and argument shapes as `hf buckets`, backed by tensordex-client.

The stock `hf` binary dispatches unknown top-level commands to an installed extension's executable
(`hf-tensordex`), so this file only maps hf-style verbs onto the client CLI. Tensor files are compressed
and reconstructed transparently; every other file passes straight through to the bucket.
"""

from __future__ import annotations

import sys

import typer

from tensordex_client.cli import app as client_app

app = typer.Typer(add_completion=False, help="TensorDex-backed storage in your Hugging Face bucket (same verbs as `hf buckets`).")

# hf buckets verbs: list|ls, cp, sync, rm|remove, info, create, delete, settings, move
for cmd in client_app.registered_commands:
    app.registered_commands.append(cmd)


def _alias(name: str, target: str, help_: str | None = None) -> None:
    src = next(c for c in client_app.registered_commands if (c.name or c.callback.__name__) == target)
    import copy
    c = copy.copy(src)
    c.name = name
    if help_:
        c.help = help_
    app.registered_commands.append(c)


_alias("list", "ls", "List logical files (alias of ls).")
_alias("remove", "rm", "Delete a file (alias of rm).")
_alias("sync", "cp", "Copy a directory to or from the bucket (alias of cp; only changed files are transferred).")


@app.command()
def status(url: str = typer.Argument(..., help="hf://buckets/<ns>/<bucket>")):
    """Binding status, savings, open findings and recent events."""
    from tensordex_client.cli import _bucket, _fmt, console
    b, _ = _bucket(url, None, "hf")
    i = b.info()
    console.print(f"[bold]{i['hf_bucket']}[/bold] [{i['status']}]  logical {_fmt(i['logical_bytes'])} → physical {_fmt(i['physical_bytes'])} "
                  f"({(1 - i['physical_bytes'] / i['logical_bytes']):.1%} saved)" if i['logical_bytes'] else f"{i['hf_bucket']} [{i['status']}] empty")
    console.print(f"retained bases {_fmt(i['retained_bytes'])} · tensors {i['tensors']:,} · open findings {i['open_findings']}")
    for e in b.api.events(b.hf_bucket, limit=10):
        console.print(f"  {e['at'][:19]}  {e['actor']:10s} {e['action']:10s} {e.get('subject') or ''}")


def main() -> None:
    try:
        app()
    except KeyboardInterrupt:
        sys.exit(130)
