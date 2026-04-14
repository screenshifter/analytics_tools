load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "optimal_credit_length_estimation",
    srcs = [
        "credit_length_estimator.py",
    ],
    main = "credit_length_estimator.py",
    data = [
        "//finance/optimal_credit_length_estimation/input:default_input.json",
    ],
    deps = [
        "//finance/optimal_credit_length_estimation/detail",
        "//finance/optimal_credit_length_estimation/credit",
        "//finance/optimal_credit_length_estimation/input",
        "//finance/optimal_credit_length_estimation/user_interface",
        "@rules_python//python/runfiles",
    ],
)
