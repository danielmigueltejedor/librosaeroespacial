def summary(values):
    if not values:
        return None
    total = 0
    for value in values:
        total += value
    return total / len(values)


def count_above(values, limit):
    count = 0
    for value in values:
        if value > limit:
            count += 1
    return count


def first_peak(values, limit):
    for index, value in enumerate(values):
        if value > limit:
            return index
    return None


assert summary([10, 20, 30]) == 20
assert summary([]) is None
assert summary([-4, -2]) == -3
assert count_above([10, 20, 20, 30], 20) == 1
assert count_above([], 0) == 0
assert first_peak([10, 20, 30], 20) == 2
assert first_peak([20], 20) is None
assert first_peak([30], 20) == 0
print("python: OK")
