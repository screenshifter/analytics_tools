load("@rules_python//python:py_test.bzl", "py_test")

py_test(
    name = "test_simple_credit",
    srcs = ["test_simple_credit.py"],
    main = "test_simple_credit.py",
    imports = ["../../../.."],
    deps = ["//finance/optimal_credit_length_estimation/credit"],
)

py_test(
    name = "test_credit_with_investment",
    srcs = ["test_credit_with_investment.py"],
    main = "test_credit_with_investment.py",
    imports = ["../../../.."],
    deps = ["//finance/optimal_credit_length_estimation/credit"],
)
