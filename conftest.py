import os
import sys

# The project is organised as a collection of standalone scripts that live in
# several directories.  Add each directory that contains an importable module
# to sys.path so the test-suite can import them by their plain module name.
_ROOT = os.path.dirname(os.path.abspath(__file__))

_MODULE_DIRS = [
    _ROOT,
    os.path.join(_ROOT, "Dataset", "YOLODataset"),
    os.path.join(_ROOT, "ShoeMeasurement"),
    os.path.join(_ROOT, "ShoeMeasurement", "images"),
]

for _d in _MODULE_DIRS:
    if _d not in sys.path:
        sys.path.insert(0, _d)
