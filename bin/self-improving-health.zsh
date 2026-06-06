#!/usr/bin/env zsh
set -euo pipefail

script_dir="${0:A:h}"
repo_root="${script_dir:h}"
python_script="${repo_root}/scripts/self_improving_health.py"

if [[ ! -f "$python_script" ]]; then
  print -u2 -- "Missing scanner: $python_script"
  exit 1
fi

exec python3 "$python_script" "$@"
