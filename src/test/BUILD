load("@rules_cc//cc:defs.bzl", "cc_test")

cc_test(
    name = "test",
    srcs = glob(["*.cpp"]),
    visibility = ["//src:__subpackages__"],
    deps = ["@googletest//:gtest_main", "//src",],
)
