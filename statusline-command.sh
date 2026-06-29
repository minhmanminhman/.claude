#!/usr/bin/env bash
# Claude Code status line: token usage display
input=$(cat)

used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
remaining_pct=$(echo "$input" | jq -r '.context_window.remaining_percentage // empty')
total_input=$(echo "$input" | jq -r '.context_window.total_input_tokens // empty')
ctx_size=$(echo "$input" | jq -r '.context_window.context_window_size // empty')
model=$(echo "$input" | jq -r '.model.display_name // empty')

if [ -n "$used_pct" ] && [ -n "$total_input" ] && [ -n "$ctx_size" ]; then
  used_int=$(printf '%.0f' "$used_pct")
  remaining_int=$(printf '%.0f' "$remaining_pct")

  # Choose color based on usage
  if [ "$used_int" -ge 80 ]; then
    color="\033[0;31m"   # red
  elif [ "$used_int" -ge 50 ]; then
    color="\033[0;33m"   # yellow
  else
    color="\033[0;32m"   # green
  fi
  reset="\033[0m"

  printf "${color}Tokens: %s / %s (%s%% used, %s%% left)${reset}" \
    "$total_input" "$ctx_size" "$used_int" "$remaining_int"
  [ -n "$model" ] && printf "  |  %s" "$model"
else
  [ -n "$model" ] && printf "%s" "$model"
fi
