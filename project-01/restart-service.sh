#!/usr/bin/env bash
#
# restart-service.sh — the verified ministry-web runbook, as a script.
# Adapted from the course starter code/restart-web-service.sh (systemd) to THIS
# lab box, where ministry-web runs as a Docker container (nginx on :8080).
# Exits 0 only if the service is HEALTHY afterward; non-zero if it is not.

set -euo pipefail

CONTAINER="ministry-web"
HEALTH_URL="http://127.0.0.1:8080/healthz"

log() { printf '%s [restart-service] %s\n' "$(date -Is)" "$*"; }

# 1. CONFIRM the container exists before we touch it.
if ! docker inspect "$CONTAINER" >/dev/null 2>&1; then
  log "ERROR: container '$CONTAINER' not found on this host. Aborting."
  exit 1
fi

# 2. CAPTURE state for the postmortem BEFORE changing anything.
log "Pre-restart status:"
docker ps -a --filter "name=$CONTAINER" --format '  {{.Names}}: {{.Status}}'
log "Last 20 log lines:"
docker logs --tail 20 "$CONTAINER" 2>&1 | sed 's/^/  /' || true

# 3. CHANGE — restart the service.
log "Restarting $CONTAINER ..."
docker restart "$CONTAINER" >/dev/null

# 4. VERIFY it is actually HEALTHY, not merely "started".
sleep 3
if curl -fsS --max-time 5 "$HEALTH_URL" | grep -q '^ok$'; then
  log "OK: $CONTAINER is healthy (HTTP 200, body 'ok')"
  exit 0
else
  log "FAIL: $CONTAINER restarted but health check FAILED. Escalate to on-call."
  docker ps -a --filter "name=$CONTAINER" --format '  {{.Names}}: {{.Status}}'
  exit 2
fi
