load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "log_crawler",
    srcs = ["log_crawler.py"],
    data = ["//misc/test_cpp_project:main"],
    deps = ["//misc/log_crawler/utils"],
)
