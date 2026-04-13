load("@rules_python//python:py_test.bzl", "py_test")

py_test(
    name = "test_investment",
    srcs = ["test_investment.py"],
    main = "test_investment.py",
    imports = ["../../../.."],
    deps = ["//finance/optimal_credit_length_estimation/detail"],
)
