#!/bin/bash
set -euo pipefail

cd "${BUILD_WORKSPACE_DIRECTORY:-"$(dirname "$(dirname "$(dirname "$(realpath "${BASH_SOURCE[0]}")")")")"}"
bazelisk coverage --config=gcc //...
bazelisk run //third_party/lcov:coverage_report -- "$@"
