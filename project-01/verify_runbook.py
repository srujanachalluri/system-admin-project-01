#!/usr/bin/env python3
"""verify_runbook.py — a linter for AI-drafted runbooks (hardened for Project 1).
Catches MECHANICAL hallucinations so the human can spend judgment on the subtle ones.
Exit 0 = no flags; 1 = flags found (a human must still review)."""
import re
import sys

DANGER = [
    (r"rm\s+-rf\s+/var/log/journal", "Deletes the systemd journal — destroys postmortem evidence."),
    (r"rm\s+-rf\s+/(?!\w*tmp)", "Recursive force-delete near a root path. A human must execute deletions."),
    (r"worker_connections\s+\d{6,}", "Absurd nginx worker_connections value — confident-but-wrong AI number."),
    (r"Restart=always-immediately", "Not a valid systemd Restart= value. Hallucinated directive."),
    (r"chmod\s+777", "World-writable permissions. Almost never the right fix."),
    (r"-f\b|--follow|--since", "A tailing/streaming command in a runbook step will block automation."),
    # --- hardened additions (Sareena Challuri) ---
    (r"\bsystemctl\b|\bjournalctl\b", "Assumes systemd — verify THIS host actually uses it (ours runs Docker)."),
    (r"is-active", "Checks the service STARTED, not that it is HEALTHY. Hit a real endpoint instead."),
    (r"ministry-webserver", "Wrong service name. The real service is 'ministry-web'; this restarts nothing."),
    (r"nginx\s+-s\s+reload", "Reloads nginx after an UNVERIFIED config edit. Confirm the root cause first."),
]


def main(path):
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        print(f"cannot read {path}: {e}", file=sys.stderr)
        return 2
    flags = 0
    for i, line in enumerate(text.splitlines(), 1):
        for pat, why in DANGER:
            if re.search(pat, line):
                print(f"  line {i:>3}: {why}")
                print(f"           > {line.strip()}")
                flags += 1
    print(f"\n{flags} automatic flag(s). A human still owns the verdict on every line.")
    return 1 if flags else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))