#ifndef SCHEDULER_HPP
#define SCHEDULER_HPP

#include <algorithm>
#include <concepts>
#include <cstdint>
#include <deque>
#include <mutex>
#include <numeric>
#include <optional>
#include <ranges>
#include <vector>
#include <functional>
#include <type_traits>
#include <utility>
#include <limits>
#include <stdexcept>

template <typename F>
concept ExecutableTask = std::invocable<F> && std::same_as<std::invoke_result_t<F>, int64_t>;

template <ExecutableTask Task>
class BoundedTaskQueue {
public:
    explicit BoundedTaskQueue(size_t capacity) : capacity_(capacity) {}

    bool try_push(Task&& task) {
        std::lock_guard<std::mutex> lock(mu_);
        if (queue_.size() >= capacity_) {
            return false;
        }
        queue_.push_back(std::move(task));
        return true;
    }

    std::optional<Task> try_pop() {
        std::lock_guard<std::mutex> lock(mu_);
        if (queue_.empty()) {
            return std::nullopt;
        }
        Task front = std::move(queue_.front());
        queue_.pop_front();
        return front;
    }

    size_t size() const {
        std::lock_guard<std::mutex> lock(mu_);
        return queue_.size();
    }

private:
    size_t capacity_;
    mutable std::mutex mu_;
    std::deque<Task> queue_;
};

inline int64_t sum_squares_of_even_above(const std::vector<int64_t>& values, int64_t threshold) {
    auto view = values
        | std::views::filter([threshold](int64_t x) { return x > threshold && (x % 2 == 0); })
        | std::views::transform([](int64_t x) {
            if (x > 3037000499LL || x < -3037000499LL) {
                throw std::overflow_error("square exceeds int64_t");
            }
            return x * x;
        });
    int64_t total = 0;
    for (int64_t v : view) {
        if (total > std::numeric_limits<int64_t>::max() - v) {
            throw std::overflow_error("sum exceeds int64_t");
        }
        total += v;
    }
    return total;
}

#endif
