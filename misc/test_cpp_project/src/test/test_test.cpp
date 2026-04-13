#include "src/test.h"

#include <gtest/gtest.h>

namespace test
{
namespace
{
TEST(FirstTest, Sum_GivenValidInput_ExpectValidAnswer)
{
    EXPECT_EQ(15, test_space::Sum(10, 5));
}

} // namespace

} // namespace test
