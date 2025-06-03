#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


def has_test_files(test_dir: Path) -> bool:
    # 检查目录中是否有 pytest 默认识别的测试文件
    patterns = ["test_*.py", "*_test.py"]
    for pattern in patterns:
        if any(test_dir.glob(pattern)):
            return True
    return False


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    test_dirs = sorted(root.glob("ch*/tests"))

    if not test_dirs:
        print("No chapter test directories found.")
        sys.exit(0)

    failed = False
    for test_dir in test_dirs:
        if has_test_files(test_dir):
            print(f"🔍 Running tests in: {test_dir}")
            result = subprocess.run(["pytest", str(test_dir)])
            if result.returncode != 0:
                failed = True
        else:
            print(f"Skipping {test_dir} (no test files found)")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
