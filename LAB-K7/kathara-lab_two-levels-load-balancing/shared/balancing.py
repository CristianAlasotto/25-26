import subprocess
import re
from collections import Counter

N = 100
counts = Counter()

for _ in range(N):
    result = subprocess.run(
        ["curl", "-s", "--connect-timeout", "2", "http://www.uniroma3.it"],
        capture_output=True,
        text=True
    )

    m = re.search(r"ws[1-4]", result.stdout, re.IGNORECASE)

    if m:
        counts[m.group(0).lower()] += 1
    else:
        counts["unknown"] += 1

for server in ["ws1", "ws2", "ws3", "ws4"]:
    n = counts[server]
    print(f"{server}: {n:3d}  ({n/N*100:.1f}%)")

if counts["unknown"]:
    print("unknown:", counts["unknown"])