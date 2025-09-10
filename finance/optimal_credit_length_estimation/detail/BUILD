load("@exdeps//:requirements.bzl", "requirement")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")
load("@rules_python//python:py_library.bzl", "py_library")

compile_pip_requirements(
    name = "requirements",
    src = "//pypi:requirements.in",
    requirements_txt = "//pypi:requirements_lock.txt",
)

py_library(
    name = "detail",
    srcs = glob(["*.py"]),
    visibility = ["//finance/optimal_credit_length_estimation:__subpackages__"],
    deps = [
        requirement("matplotlib"),
    ],
)
