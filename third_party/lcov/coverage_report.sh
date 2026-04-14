#!/bin/bash
set -euo pipefail

REPORT_DIR="$HOME/workspace/tmp/${1:-coverage_report}"
LCOV_DATA="$BUILD_WORKSPACE_DIRECTORY/bazel-out/_coverage/_coverage_report.dat"
RUNFILES="${BASH_SOURCE[0]}.runfiles"
GENHTML="$RUNFILES/lcov~/genhtml"

RUNFILES_DIR="$RUNFILES" \
RUNFILES_MANIFEST_FILE="${BASH_SOURCE[0]}.runfiles_manifest" \
    "$GENHTML" "$LCOV_DATA" \
    --output-directory "$REPORT_DIR" \
    --source-directory "$BUILD_WORKSPACE_DIRECTORY" \
    --ignore-errors unsupported,source
echo "Report generated at $REPORT_DIR/index.html"
