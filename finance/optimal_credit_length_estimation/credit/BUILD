load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "credit",
    srcs = glob(["*.py"]),
    visibility = ["//finance/optimal_credit_length_estimation:__subpackages__"],
    deps = ["//finance/optimal_credit_length_estimation/detail"],
)
