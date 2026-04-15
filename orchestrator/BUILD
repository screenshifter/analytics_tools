load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "orchestrator",
    srcs = glob(["*.py"]),
    visibility = ["//visibility:public"],
    deps = [
        "//finance/optimal_credit_length_estimation:optimal_credit_length_estimation_lib",
        "@rules_python//python/runfiles",
    ],
)
