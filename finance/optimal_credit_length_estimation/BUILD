# load("@rules_python//python:defs.bzl", "py_binary")
load("@rules_python//python:py_binary.bzl", "py_binary")

py_binary(
    name = "optimal_credit_length_estimation",
    srcs = [
        "credit_length_estimator.py",
        # "detail/input.py",
        # "detail/simple_credit.py",
        # "detail/visualization.py",
    ],
    main = "credit_length_estimator.py",
    deps = [
        "//common",
        "//finance/optimal_credit_length_estimation/detail",
    ],
)
