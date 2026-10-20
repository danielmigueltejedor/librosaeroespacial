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
    std::cout << "cpp-task-scheduler ok: acc=" << acc << ", ranges_sum=" << res << "\n";
    return 0;
}
