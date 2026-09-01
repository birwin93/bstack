#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <agent-skills-directory>" >&2
  exit 64
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd "${script_dir}/.." && pwd)"
source_dir="${repo_dir}/skills"
target_dir="${1%/}"
conflicts=0

mkdir -p "${target_dir}"

for source in "${source_dir}"/*; do
  [[ -d "${source}" ]] || continue
  name="$(basename "${source}")"
  target="${target_dir}/${name}"

  if [[ -L "${target}" && "$(readlink "${target}")" == "${source}" ]]; then
    echo "already linked: ${name}"
  elif [[ -e "${target}" || -L "${target}" ]]; then
    echo "conflict: ${target}" >&2
    conflicts=$((conflicts + 1))
  else
    ln -s "${source}" "${target}"
    echo "linked: ${name}"
  fi
done

if [[ ${conflicts} -ne 0 ]]; then
  echo "left ${conflicts} existing skill path(s) unchanged" >&2
  exit 1
fi
