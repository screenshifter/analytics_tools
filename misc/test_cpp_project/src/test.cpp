#include "src/test.h"

#include <cstddef>
#include <iostream>

namespace test_space
{
std::size_t Sum(std::size_t first, std::size_t second)
{
    return first + second;
}

TestClass::TestClass(std::size_t value) : value_{value}
{
    std::cout << "Constructed with value " << value_ << "\n";
}

TestClass::~TestClass()
{
    std::cout << "Destructed with value " << value_ << "\n";
}

} // namespace test_space
