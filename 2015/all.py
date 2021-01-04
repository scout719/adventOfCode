# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
# pylint: enable=wrong-import-position

""" MAIN FUNCTION """

if __name__ == "__main__":
    import importlib
    import inspect
    for i in range(1, 26):
        try:
            m = importlib.import_module(f"day{i}")
            for k, v in inspect.getmembers(m):
                if k in [f"day{i}_1", f"day{i}_2"]:
                    globals()[k] = v
        except ModuleNotFoundError:
            pass
    main(sys.argv, globals(), 2015)
