load("@rules_cc//cc:defs.bzl", "cc_library")

cc_library(
    name = "src",
    srcs = glob(["*.cpp"]),
    hdrs = glob(["*.h"]),
    strip_include_prefix = "/misc/test_cpp_project",
    visibility = ["//misc/test_cpp_project:__subpackages__"],
)
