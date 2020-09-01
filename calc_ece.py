import numpy as np
import argparse

from utils import *
from calibration_utils import *


def parse_args():
    parser = argparse.ArgumentParser(description="Calculate inference ECE")
    parser.add_argument("--prob", default="prob.txt")
    parser.add_argument("--trans", default="trans.txt")
    parser.add_argument("--label", default="label.txt")
    parser.add_argument("--vocabulary", default="vocab.en.txt")
    parser.add_argument("--bins", type=int, default=20)
    parser.add_argument("--partition", default="uniform")

    return parser.parse_args()


def main(args):
    prob = file2words(args.prob, chain=True)
    trans = file2words(args.trans, chain=True)
    label = file2words(args.label, chain=True)

    prob = [np.exp(float(p)) for p in prob]
    float_label = []
    for ll in label:
        if ll == 'C' or ll == '1' or ll == '1.0':
            float_label.append(1.0)
        else:
            float_label.append(0.0)
    vocab = load_vocab(args.vocabulary)

    if args.partition == "uniform":
        err_mtrx, hit_mtrx, _, count_mtrx = error_matrix_uniform(prob, trans, float_label, vocab, bins=args.bins)
    elif args.partition == "balanced":
        err_mtrx, hit_mtrx, _, count_mtrx, _ = error_matrix_balanced(prob, trans, float_label, vocab, bins=args.bins)

    abs_ece = calculate_ece(err_mtrx, count_mtrx) * 100
    # token_ece = calculate_token_ece(err_mtrx, count_mtrx)
    # rel_ece = np.sqrt(calculate_sharpness(err_mtrx, count_mtrx)) * 100
    # sharp = np.sqrt(calculate_sharpness(hit_mtrx, count_mtrx)) * 100
    # ppl = np.exp(np.mean([-np.log(p) for p in prob]))

    # print("{:.2f}\t{:.2f}\t{:.2f}\t{:.4f}\t{:.4f}\t{:.2f}".format(abs_ece, rel_ece, sharp, np.mean(prob), np.mean(float_label), ppl))
    print("{:.2f}\t{:.4f}".format(abs_ece, np.mean(prob)))


if __name__ == '__main__':
    main(parse_args())
