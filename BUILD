load("@rules_cc//cc:defs.bzl", "cc_binary")

cc_binary(
    name = "main",
    srcs = ["main.cc"],
    deps = ["//src"],
    visibility = ["//visibility:public"],
)

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

exports_files([".clang-tidy", ".clang-tidy-pedantic"])
