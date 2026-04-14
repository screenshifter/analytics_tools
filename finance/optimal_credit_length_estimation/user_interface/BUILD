load("@pypi//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "user_interface",
    srcs = ["visualization.py"],
    visibility = ["//finance/optimal_credit_length_estimation:__subpackages__"],
    deps = [
        "//finance/optimal_credit_length_estimation/detail",
        requirement("matplotlib"),
    ],
)
