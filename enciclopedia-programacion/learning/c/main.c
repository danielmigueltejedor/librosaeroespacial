#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>

bool maximum(const int *values, size_t n, int *out) {
    if (n == 0) return false;
    int best = values[0];
    for (size_t i = 1; i < n; ++i) {
        if (values[i] > best) best = values[i];
    }
    *out = best;
    return true;
}
size_t count_byte(const char *text, size_t n, char target) {
    size_t count = 0;
    for (size_t i = 0; i < n; ++i) {
        if (text[i] == target) ++count;
    }
    return count;
}
bool copy_text(char *dst, size_t capacity, const char *src) {
    size_t n = strlen(src);
    if (n >= capacity) return false;
    memcpy(dst, src, n + 1);
    return true;
}
int main(void) {
    int result = 99;
    int values[] = {-4, -2, -7};
    assert(maximum(values, 3, &result) && result == -2);
    assert(!maximum(NULL, 0, &result) && result == -2);
    assert(count_byte("aba", 3, 'a') == 2);
    assert(count_byte(NULL, 0, 'a') == 0);
    char dst[4] = "old";
    assert(copy_text(dst, sizeof dst, "abc"));
    assert(strcmp(dst, "abc") == 0);
    assert(!copy_text(dst, sizeof dst, "abcd"));
    assert(strcmp(dst, "abc") == 0);
    assert(copy_text(dst, sizeof dst, ""));
    assert(!copy_text(NULL, 0, ""));
    int one[] = {7};
    assert(maximum(one, 1, &result) && result == 7);
    puts("c: OK");
}
