import os
import sys


def find_binary():
    manifest = os.environ.get("RUNFILES_MANIFEST_FILE")
    if manifest:
        with open(manifest) as f:
            for line in f:
                key, _, path = line.strip().partition(" ")
                if key == "_main/main":
                    return path
    return sys.argv[1] if len(sys.argv) > 1 else "bazel-bin/main"
