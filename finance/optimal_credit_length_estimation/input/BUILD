load("@rules_python//python:defs.bzl", "py_library")

exports_files(["default_input.json"])

py_library(
    name = "input",
    srcs = ["input.py"],
    visibility = ["//finance/optimal_credit_length_estimation:__subpackages__"],
    deps = ["//common"],
)
