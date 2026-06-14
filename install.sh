#!/usr/bin/env bash
# REINS Method installer
#
#   curl -fsSL https://raw.githubusercontent.com/gustavodiasp/reins-method/main/install.sh | bash
#
# Clones REINS Method into ~/.reins (or pulls latest if already installed) and
# launches the interactive setup wizard.

set -euo pipefail

# Warm orange -> amber gradient. Falls back to plain text when not attached
# to a color-capable terminal (e.g. piped logs).
if [ -t 1 ] && [ "${TERM:-}" != "dumb" ]; then
  C1='\033[38;5;208m'; C2='\033[38;5;209m'; C3='\033[38;5;215m'
  C4='\033[38;5;221m'; C5='\033[38;5;222m'; C6='\033[38;5;223m'
  C7='\033[38;5;224m'
  BOLD='\033[1m'; RESET='\033[0m'
else
  C1=''; C2=''; C3=''; C4=''; C5=''; C6=''; C7=''; BOLD=''; RESET=''
fi

printf "%b\n" \
"${C1}█████ █████ ███ █   █  ████${RESET}" \
"${C2}█   █ █      █  ██  █ █${RESET}" \
"${C3}█   █ █      █  █ █ █ █${RESET}" \
"${C4}█████ ████   █  █  ██  ███${RESET}" \
"${C5}█ █   █      █  █   █     █${RESET}" \
"${C6}█  █  █      █  █   █     █${RESET}" \
"${C7}█   █ █████ ███ █   █ ████${RESET}" \
"" \
"${BOLD}AI is like a horse — strong, but it goes where it wants without a rider.${RESET}" \
"${BOLD}REINS is the bridle.${RESET}" \
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
