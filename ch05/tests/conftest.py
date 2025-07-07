# ch05/tests/conftest.py
import sys
from pathlib import Path

# 添加项目根目录到 sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))
print(str(Path(__file__).resolve().parents[1]))
