load("@rules_shell//shell:sh_binary.bzl", "sh_binary")

sh_binary(
    name = "coverage",
    srcs = ["coverage.sh"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "coverage_report",
    srcs = ["coverage_report.sh"],
    data = ["@lcov//:genhtml"],
    visibility = ["//visibility:public"],
)
