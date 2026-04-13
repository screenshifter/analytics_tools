#include "src/test.h"

#include <cstddef>
#include <iostream>

int main()
{
    constexpr std::size_t kFirstArgument{5U};
    constexpr std::size_t kSecondArgument{14U};
    constexpr std::size_t kTestValue{16U};

    [[maybe_unused]] const test_space::TestClass test_val{kTestValue};

    std::cout << "Hello, Bazel + GCC!\n";
    std::cout << "5 + 14 is "
              << test_space::Sum(kFirstArgument, kSecondArgument) << "\n";

    return 0;
}
