#include "scheduler.hpp"
#include <cassert>
#include <functional>
#include <iostream>

int main() {
    BoundedTaskQueue<std::function<int64_t()>> q(3);
    assert(q.try_push([]() -> int64_t { return 10; }));
    assert(q.try_push([]() -> int64_t { return 20; }));
    assert(q.try_push([]() -> int64_t { return 30; }));
    assert(!q.try_push([]() -> int64_t { return 40; })); // capacidad máxima 3

    int64_t acc = 0;
    while (auto task = q.try_pop()) {
        acc += (*task)();
    }
    assert(acc == 60);

    std::vector<int64_t> sample{1, 2, 4, 5, 6, 8, 9, 10};
    int64_t res = sum_squares_of_even_above(sample, 3); // 4^2 + 6^2 + 8^2 + 10^2 = 16+36+64+100 = 216
    assert(res == 216);
    assert(sum_squares_of_even_above({-4, -3, 2}, -5) == 20);
    assert(sum_squares_of_even_above({}, 0) == 0);
    bool caught = false;
    try { (void)sum_squares_of_even_above({INT64_MIN}, INT64_MIN); }
    catch (const std::overflow_error&) { caught = true; }
    assert(!caught); // filtered by strict threshold before squaring
    caught = false;
    try { (void)sum_squares_of_even_above({4000000000LL}, 0); }
    catch (const std::overflow_error&) { caught = true; }
    assert(caught);
    caught = false;
    try { (void)sum_squares_of_even_above({3000000000LL, 3000000000LL}, 0); }
    catch (const std::overflow_error&) { caught = true; }
    assert(caught);
    std::cout << "cpp-task-scheduler ok: acc=" << acc << ", ranges_sum=" << res << "\n";
    return 0;
}
