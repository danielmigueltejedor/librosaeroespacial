#!/usr/bin/env bash
list_txt() {
    local file
    for file in "$1"/*.txt; do
        [ -f "$file" ] || continue
        printf '%s\n' "$file"
    done
}
count_args() {
    printf '%s\n' "$#"
}
first_line() {
    local line
    [ -f "$1" ] || return 2
    IFS= read -r line < "$1" || [ -n "$line" ] || return 1
    printf '%s\n' "$line"
}
