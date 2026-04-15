load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "user_interface",
    srcs = glob(["*.py", "pages/*.py"]),
    visibility = ["//visibility:public"],
    deps = [
        "//orchestrator",
        "@pypi//streamlit",
    ],
)
