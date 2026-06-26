# Project 1 — From Runbook to Copilot
St. Augustine "ministry-web" incident runbook + AI-copilot evaluation.
Author / accountable steward: **Sareena Challuri**

## Files
- `runbook-verified.txt` — hand-built, verified runbook (confirm→capture→change→verify)
- `restart-service.sh`   — runnable version; exits non-zero on health failure
- `runbook-ai.txt`       — UNEDITED AI draft (Claude Opus 4.8) of the same task
- `verdict.txt`          — line-by-line verified/wrong/unsafe comparison
- `verify_runbook.py`    — hardened linter for AI-drafted runbooks
- `copilot_policy.yaml`  — AI usage policy for the parish
- `REPORT.docx`          — write-up + honest AI usage note

## Lab
GitHub Codespaces (Ubuntu + Docker). ministry-web runs as an nginx container on :8080 with /healthz.

## Reproduce (grader)
    docker run -d --name ministry-web -p 8080:8080 \
      -v "$PWD/ministry-web/default.conf:/etc/nginx/conf.d/default.conf:ro" nginx:stable
    curl -fsS http://127.0.0.1:8080/healthz     # -> ok
    ./restart-service.sh; echo "exit=$?"        # -> exit=0 when healthy
    python3 verify_runbook.py runbook-ai.txt    # -> several flags on the AI draft

## AI usage (Phase 1)
Claude Opus 4.8 was used to scaffold the lab, script, and linter, and to generate `runbook-ai.txt`.
The verified runbook was written and RUN by the human, who owns every verdict. See REPORT.docx.
