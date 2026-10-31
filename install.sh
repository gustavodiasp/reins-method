#!/usr/bin/env bash
# REINS Method installer
#
#   curl -fsSL https://raw.githubusercontent.com/gustavodiasp/reins-method/main/install.sh | bash
#
# Clones REINS Method into ~/.reins (or pulls latest if already installed) and
# launches the interactive setup wizard.

set -euo pipefail

# Green palette. Falls back to plain text when not attached to a
# color-capable terminal (e.g. piped logs).
if [ -t 1 ] && [ "${TERM:-}" != "dumb" ]; then
  HORSE='\033[32m'; REINS='\033[92m'; MUTED='\033[2;32m'; RESET='\033[0m'
else
  HORSE=''; REINS=''; MUTED=''; RESET=''
fi

printf "%b\n" \
"${HORSE}      ,~~_              ${REINS}____  ___________   _______${RESET}" \
"${HORSE}      |/\\ =_ _ ~       ${REINS}/ __ \\/ ____/  _/ | / / ___/${RESET}" \
"${HORSE}       _( )_( )\\~~    ${REINS}/ /_/ / __/  / //  |/ /\\__ \\${RESET}" \
"${HORSE}       \\,\\  _|\\ \\~~~ ${REINS}/ _, _/ /____/ // /|  /___/ /${RESET}" \
"${HORSE}          \\\`   \\    ${REINS}/_/ |_/_____/___/_/ |_//____/${RESET}" \
"${HORSE}          \`    \`${RESET}" \
"" \
"${MUTED}  Structured AI pair programming method${RESET}" \
"${MUTED}  ──────────────────────────────────────────────────${RESET}" \
"  Agent-agnostic · stack-agnostic · globally installed" \
""

REPO_URL="${REINS_REPO_URL:-https://github.com/gustavodiasp/reins-method.git}"
REINS_HOME="${REINS_HOME:-$HOME/.reins}"

command -v git >/dev/null 2>&1 || { echo "Error: git is required." >&2; exit 1; }

echo ""
if [ -x "$REINS_HOME/bin/reins" ]; then
  echo "REINS Method already installed at $REINS_HOME — updating..."
  "$REINS_HOME/bin/reins" update
elif [ -e "$REINS_HOME" ]; then
  echo "Error: $REINS_HOME exists but doesn't look like a REINS installation. Move it aside first." >&2
  exit 1
else
  # Clone to a temp dir, never directly into $REINS_HOME: cloning in place
  # would leave .git/, .github/, and every root dev file (README.md,
  # MIGRATION.md, etc.) sitting permanently inside the live install, since
  # install_core_files() — the only thing that strips those — only runs when
  # $CORE_DIR doesn't already exist, which a direct clone defeats.
  tmp_dir="$(mktemp -d "${TMPDIR:-/tmp}/reins-install.XXXXXX")"
  trap 'rm -rf "$tmp_dir"' EXIT
  echo "Downloading REINS Method..."
  git clone --depth 1 "$REPO_URL" "$tmp_dir" >/dev/null
  chmod +x "$tmp_dir/bin/reins"
  "$tmp_dir/bin/reins" install --from-package="$tmp_dir"
fi
