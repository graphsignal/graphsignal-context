import sys
import pytest


def main():
    args = ["tests/", "-v"] + sys.argv[1:]
    sys.exit(pytest.main(args))
