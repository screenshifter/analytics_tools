import subprocess

from misc.log_crawler.utils.os_utils import find_binary

result = subprocess.run([find_binary()], capture_output=True, text=True)
output = (result.stdout + result.stderr).strip()

print(f"C++ program finished with code {result.returncode}, printed strings are: {output}")
