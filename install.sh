#!/usr/bin/env bash
# PAW Method installer
#
#   curl -fsSL https://raw.githubusercontent.com/gustavodiasp/paw-method/main/install.sh | bash
#
# Clones PAW Method into ~/.paw (or pulls latest if already installed) and
# launches the interactive setup wizard.

set -euo pipefail

# Warm orange -> amber gradient, paw-print themed. Falls back to plain text
# when not attached to a color-capable terminal (e.g. piped logs).
if [ -t 1 ] && [ "${TERM:-}" != "dumb" ]; then
  C1='\033[38;5;208m'; C2='\033[38;5;209m'; C3='\033[38;5;215m'
  C4='\033[38;5;221m'; C5='\033[38;5;222m'; C6='\033[38;5;223m'
  BOLD='\033[1m'; RESET='\033[0m'
else
  C1=''; C2=''; C3=''; C4=''; C5=''; C6=''; BOLD=''; RESET=''
fi

printf "%b\n" \
"${C1} @@@@@@@    @@@@@@   @@@  @@@  @@@${RESET}" \
"${C2}@@@@@@@@  @@@@@@@@  @@@  @@@  @@@${RESET}" \
"${C3}@@!  @@@  @@!  @@@  @@!  @@!  @@!${RESET}" \
"${C4}!@!  @!@  !@!  @!@  !@!  !@!  !@!${RESET}" \
"${C5}@!@@!@!   @!@!@!@!  @!!  !!@  @!@${RESET}" \
"${C6}!!@!!!    !!!@!!!!  !@!  !!!  !@!${RESET}" \
"${C1}!!:       !!:  !!!  !!:  !!:  !!:${RESET}" \
"${C2}:!:       :!:  !:!  :!:  :!:  :!:${RESET}" \
"${C3} ::       ::   :::   :::: :: :::${RESET}" \
"${C4} :         :   : :    :: :  : :${RESET}" \
"" \
"${BOLD}      Purposeful AI Workflow Method${RESET}" \
""

REPO_URL="${PAW_REPO_URL:-https://github.com/gustavodiasp/paw-method.git}"
PAW_HOME="${PAW_HOME:-$HOME/.paw}"

command -v git >/dev/null 2>&1 || { echo "Error: git is required." >&2; exit 1; }

if [ -d "$PAW_HOME/.git" ]; then
  echo "PAW Method already installed at $PAW_HOME — pulling latest core..."
  git -C "$PAW_HOME" pull --ff-only
elif [ -e "$PAW_HOME" ]; then
  echo "Error: $PAW_HOME exists and is not a PAW git checkout. Move it aside first." >&2
  exit 1
else
  echo "Cloning PAW Method to $PAW_HOME..."
  git clone --depth 1 "$REPO_URL" "$PAW_HOME"
fi

chmod +x "$PAW_HOME/bin/paw"

echo ""
"$PAW_HOME/bin/paw" install
