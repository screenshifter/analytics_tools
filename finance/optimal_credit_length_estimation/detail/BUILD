load("@pypi//:requirements.bzl", "requirement")
load("@rules_python//python:py_library.bzl", "py_library")

py_library(
    name = "detail",
    srcs = glob(["*.py"]),
    visibility = ["//finance/optimal_credit_length_estimation:__subpackages__"],
    deps = [
        requirement("matplotlib"),
    ],
)
