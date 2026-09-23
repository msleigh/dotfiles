#!/usr/bin/env bash

set -euo pipefail

# Load machine-local credentials when this is run outside an interactive shell.
if [[ -f "${HOME}/.extra" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${HOME}/.extra"
  set +a
fi

: "${JELLYFIN_URL:=http://pi01.local:8096}"
if [[ -z "${JELLYFIN_API_KEY:-}" ]]; then
  printf 'error: JELLYFIN_API_KEY is not set
' >&2
  exit 2
fi

base_url="${JELLYFIN_URL%/}"

jellyfin_curl() {
  # Passing curl configuration on stdin keeps the API key out of argv and output.
  printf 'header = "X-Emby-Token: %s"
' "${JELLYFIN_API_KEY}" |
    curl --config - --fail --silent --show-error --max-time 30 "${@}"
}

case "${1:-refresh}" in
  refresh)
    tasks="$(jellyfin_curl "${base_url}/ScheduledTasks")"
    already_running="$(jq -r 'any(.[]; (.Name == "Scan Media Library" or .Key == "RefreshLibrary") and .State == "Running")' <<<"${tasks}")"
    if [[ "${already_running}" == "true" ]]; then
      jq -n '{accepted: false, already_running: true, status: null}'
    else
      status="$(jellyfin_curl --output /dev/null --write-out '%{http_code}'         --request POST "${base_url}/Library/Refresh")"
      jq -n --arg status "${status}"         '{accepted: ($status == "204"), already_running: false, status: ($status | tonumber)}'
    fi
    ;;
  status)
    jellyfin_curl "${base_url}/ScheduledTasks" |
      jq '[.[] | select(.Name == "Scan Media Library" or .Key == "RefreshLibrary") |
        {name: .Name, state: .State, progress: .CurrentProgressPercentage,
         last_result: .LastExecutionResult}]'
    ;;
  search)
    if [[ -z "${2:-}" ]]; then
      printf 'usage: %s search TITLE
' "${0}" >&2
      exit 2
    fi
    jellyfin_curl --get       --data-urlencode "SearchTerm=${2}"       --data-urlencode 'Recursive=true'       --data-urlencode 'IncludeItemTypes=Movie,Episode'       --data-urlencode 'Fields=Path,ProviderIds'       "${base_url}/Items" |
      jq '[.Items[] | {name: .Name, year: .ProductionYear, path: .Path,
        provider_ids: .ProviderIds, id: .Id}]'
    ;;
  *)
    printf 'usage: %s [refresh|status|search TITLE]
' "${0}" >&2
    exit 2
    ;;
esac
