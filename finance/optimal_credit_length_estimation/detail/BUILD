load("@pypi//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "detail",
    srcs = glob(["*.py"]),
    visibility = ["//finance/optimal_credit_length_estimation:__subpackages__"],
    deps = [
        "//common",
        requirement("matplotlib"),
    ],
)
