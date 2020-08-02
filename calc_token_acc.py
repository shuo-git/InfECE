import numpy as np
import argparse

from utils import *
from calibration_utils import *
import itertools


def parse_args():
    parser = argparse.ArgumentParser(description="Calculate the token acc")
    parser.add_argument("--input", default="input.txt")

    return parser.parse_args()


def delete_pad(_list):
    res_list = []
    for item in _list:
        if item == '2.0':
            break
        res_list.append(item)
    return res_list


def main(args):
    lines = file2lines(args.input)
    lines = [l.split('|||') for l in lines]
    indices = [int(l[0]) for l in lines]
    probs = [delete_pad(l[1].split())[:-1] for l in lines]
    accs = [delete_pad(l[2].split())[:-1] for l in lines]
    # data = list(zip(indices, probs, accs))
    # data.sort(key=lambda x: x[0])
    # indices, probs, accs = list(zip(*data))
    total_accs = list(itertools.chain(*accs))
    total_accs = [float(x) for x in total_accs]
    print(np.mean(total_accs))


if __name__ == '__main__':
    main(parse_args())
