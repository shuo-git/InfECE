from nltk.util import ngrams
from collections import Counter
import numpy as np
import itertools
from utils import *
from calibration_utils import *

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Label n-gram in the hypothesis")
    parser.add_argument("--hyp", default="hyp.txt")
    parser.add_argument("--ref", default="ref.txt")

    return parser.parse_args()


def label_n_gram(reference, hypothesis, n):
    ref_n_grams = Counter(ngrams(reference, n)) if len(reference) >= n else Counter()

    hit = 0
    for i in range(0, len(hypothesis) - n + 1):
        pattern = tuple(hypothesis[i:i + n])
        if ref_n_grams[pattern] > 0:
            hit += 1
            ref_n_grams[pattern] -= 1

    return hit, len(hypothesis) - n + 1, len(reference) - n + 1


def main(args):
    hyps = file2words(args.hyp)
    refs = file2words(args.ref)
    hits = [0., 0., 0., 0.]
    hyp_lens = [0., 0., 0., 0.]
    ref_lens = [0., 0., 0., 0.]
    for hyp, ref in zip(hyps, refs):
        for i in range(4):
            h, hl, rl = label_n_gram(ref, hyp, i + 1)
            hits[i] += h
            hyp_lens[i] += hl
            ref_lens[i] += rl

    print(' \t{}\t{}'.format('Precision', 'Recall'))
    for i in range(4):
        print('{}-gram\t{:.4f}\t\t{:.4f}'.format(i + 1, hits[i] / hyp_lens[i], hits[i] / ref_lens[i]))


if __name__ == '__main__':
    main(parse_args())
