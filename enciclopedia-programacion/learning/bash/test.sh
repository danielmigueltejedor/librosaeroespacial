#!/usr/bin/env bash
set -eu
source "$(dirname "$0")/main.sh"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
mkdir "$work/empty"
printf 'alpha\nbeta\n' > "$work/a b.txt"
printf 'no newline' > "$work/last.txt"
[ "$(list_txt "$work/empty")" = '' ]
[ "$(list_txt "$work" | wc -l | tr -d ' ')" = 2 ]
[ "$(count_args 'a b' '*')" = 2 ]
[ "$(count_args)" = 0 ]
[ "$(first_line "$work/a b.txt")" = alpha ]
[ "$(first_line "$work/last.txt")" = 'no newline' ]
if first_line "$work/missing"; then exit 1; else [ "$?" = 2 ]; fi
: > "$work/emptyfile"
if first_line "$work/emptyfile"; then exit 1; else [ "$?" = 1 ]; fi
printf '%s\n' ' a\b ' > "$work/spaces"
[ "$(first_line "$work/spaces")" = ' a\b ' ]
printf 'bash: OK\n'
