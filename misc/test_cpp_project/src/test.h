#ifndef SRC_TEST_H
#define SRC_TEST_H

#include <cstddef>

namespace test_space
{
std::size_t Sum(std::size_t first, std::size_t second);

class TestClass
{
  public:
    TestClass(std::size_t value);
    ~TestClass();

    TestClass(const TestClass &) = default;
    TestClass(TestClass &&) = default;

    TestClass &operator=(const TestClass &) = default;
    TestClass &operator=(TestClass &&) = default;

  private:
    std::size_t value_;
};

} // namespace test_space

#endif // SRC_TEST_H
