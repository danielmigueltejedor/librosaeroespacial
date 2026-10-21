package main
import (
    "fmt"
    "strconv"
)
func parsePort(text string) (int, error) {
    port, err := strconv.Atoi(text)
    if err != nil || port < 1 || port > 65535 {
        return 0, fmt.Errorf("invalid port: %q", text)
    }
    return port, nil
}
func frequencies(statuses []string) map[string]int {
    result := make(map[string]int)
    for _, status := range statuses { result[status]++ }
    return result
}
func validateRange(low, high int) error {
    if low > high { return fmt.Errorf("reversed range") }
    return nil
}
func check(ok bool) {
    if !ok { panic("test failed") }
}
func main() {
    p, err := parsePort("8080")
    check(err == nil && p == 8080)
    for _, text := range []string{"0", "65536", "abc", ""} {
        _, err = parsePort(text); check(err != nil)
    }
    for _, text := range []string{"1", "65535"} {
        _, err = parsePort(text); check(err == nil)
    }
    counts := frequencies([]string{"ok", "bad", "ok"})
    check(counts["ok"] == 2 && counts["missing"] == 0)
    check(len(frequencies(nil)) == 0)
    check(validateRange(3, 3) == nil)
    check(validateRange(4, 3) != nil)
    fmt.Println("go: OK")
}
