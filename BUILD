load("@rules_python//python:defs.bzl", "py_binary")

filegroup(
    name = "clang_tidy_config",
    srcs = [".clang-tidy"],
    visibility = ["//visibility:public"],
)

filegroup(
    name = "clang_tidy_pedantic_config",
    srcs = [".clang-tidy-pedantic"],
    visibility = ["//visibility:public"],
)

exports_files([
    ".clang-tidy",
    ".clang-tidy-pedantic",
])

py_binary(
    name = "analytics_tools",
    srcs = ["main.py"],
    main = "main.py",
    data = [
        "//finance/optimal_credit_length_estimation/input:default_input.json",
        "//user_interface:user_interface",
    ],
    deps = [
        "//orchestrator",
        "//user_interface",
        "@pypi//streamlit",
        "@rules_python//python/runfiles",
    ],
)
