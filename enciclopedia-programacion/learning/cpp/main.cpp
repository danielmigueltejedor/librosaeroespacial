#include <cassert>
#include <iostream>
#include <map>
#include <string>
#include <vector>

std::map<std::string, int> frequencies(const std::vector<std::string>& words) {
    std::map<std::string, int> result;
    for (const auto& word : words) ++result[word];
    return result;
}
int lookup(const std::map<std::string, int>& counts, const std::string& word) {
    auto found = counts.find(word);
    return found == counts.end() ? 0 : found->second;
}
std::vector<std::string> repeated(const std::map<std::string, int>& counts) {
    std::vector<std::string> result;
    for (const auto& [word, count] : counts) {
        if (count >= 2) result.push_back(word);
    }
    return result;
}
int main() {
    auto counts = frequencies({"sol", "luna", "sol"});
    assert(lookup(counts, "sol") == 2);
    assert(lookup(counts, "mar") == 0);
    assert(counts.size() == 2);
    assert(frequencies({}).empty());
    assert(repeated(counts) == std::vector<std::string>{"sol"});
    assert(repeated({}).empty());
    assert((repeated({{"z", 3}, {"a", 2}, {"b", 1}}) == std::vector<std::string>{"a", "z"}));
    std::cout << "cpp: OK\n";
}
