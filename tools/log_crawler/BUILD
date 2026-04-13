load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "log_crawler",
    srcs = ["log_crawler.py"],
    data = ["//:main"],
    deps = ["//tools/log_crawler/utils"],
)
