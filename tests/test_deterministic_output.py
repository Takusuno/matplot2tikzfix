"""Assert repeated exports of the same plot produce the same output file."""

import subprocess
import sys
import tempfile
from pathlib import Path

# We create the tikz files in separate subprocesses, as when producing those in
# the same process, the order of axis parameters is deterministic.
plot_code = """
import sys
import numpy as np
from matplotlib import pyplot as plt
import matplot2tikz

t = np.arange(0.0, 2.0, 0.1)
s = np.sin(2 * np.pi * t)
plt.plot(t, s, label="a")
plt.legend()
matplot2tikz.save(sys.argv[1])
"""


def test() -> None:
    _, tmp_base = tempfile.mkstemp()
    # trade-off between test duration and probability of false negative
    n_tests = 2
    tikzs = []
    for _ in range(n_tests):
        tikz_file = tmp_base + "_tikz.tex"
        try:
            _ = subprocess.check_output(  # noqa: S603
                [sys.executable, "-", tikz_file],
                input=plot_code.encode(),
                stderr=subprocess.STDOUT,
                shell=False,
            )
            sp = subprocess.Popen(  # noqa: S603
                [sys.executable, "-", tikz_file],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=False,
            )
            _, _ = sp.communicate(plot_code.encode())
        except subprocess.CalledProcessError as e:
            print("Command output:")  # noqa: T201
            print("=" * 70)  # noqa: T201
            print(e.output)  # noqa: T201
            print("=" * 70)  # noqa: T201
            raise
        with Path(tikz_file).open() as f:
            tikzs.append(f.read())
    for t in tikzs[1:]:
        assert t == tikzs[0]
