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
"${MUTED}  structured AI pair programming method${RESET}" \
"${MUTED}  ──────────────────────────────────────────────────${RESET}" \
"  agent-agnostic · stack-agnostic · globally installed" \
""

REPO_URL="${REINS_REPO_URL:-https://github.com/gustavodiasp/reins-method.git}"
REINS_HOME="${REINS_HOME:-$HOME/.reins}"

command -v git >/dev/null 2>&1 || { echo "Error: git is required." >&2; exit 1; }

if [ -d "$REINS_HOME/.git" ]; then
  echo "REINS Method already installed at $REINS_HOME — pulling latest core..."
  git -C "$REINS_HOME" pull --ff-only
elif [ -e "$REINS_HOME" ]; then
  echo "Error: $REINS_HOME exists and is not a REINS git checkout. Move it aside first." >&2
  exit 1
else
  echo "Cloning REINS Method to $REINS_HOME..."
  git clone --depth 1 "$REPO_URL" "$REINS_HOME"
fi

chmod +x "$REINS_HOME/bin/reins"

echo ""
"$REINS_HOME/bin/reins" install
