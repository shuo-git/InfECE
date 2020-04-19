from utils import *
import sys


def main():
    lines = file2lines(sys.argv[1])
    lines = add_seg_id(lines)
    lines2file(lines, sys.argv[2])


if __name__ == "__main__":
    main()
