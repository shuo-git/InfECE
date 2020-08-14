from nltk.util import ngrams
from collections import Counter
from utils import *

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Label n-gram in the hypothesis")
    parser.add_argument("--hyp", default="hyp.txt")
    parser.add_argument("--ref", default="ref.txt")
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--out_prefix", default="output.txt")

    return parser.parse_args()


def label_n_gram(reference, hypothesis, n):
    ref_n_grams = Counter(ngrams(reference, n)) if len(reference) >= n else Counter()
    labels = []
    for i in range(n - 1):
        labels.append(0)
    for i in range(0, len(hypothesis) - n + 1):
        pattern = tuple(hypothesis[i:i+n])
        if ref_n_grams[pattern] > 0:
            labels.append(1)
            ref_n_grams[pattern] -= 1
        else:
            labels.append(0)
    return labels


def label_sentence(reference, hypothesis, n):
    labels_list = []
    for i in range(1, n+1):
        labels_list.append(label_n_gram(reference, hypothesis, i))
    return labels_list


def main(args):
    hyps = file2words(args.hyp)
    refs = file2words(args.ref)
    all_labels_list = []
    for hyp, ref in zip(hyps, refs):
        labels_list = label_sentence(ref, hyp, args.n)
        all_labels_list.append(labels_list)
    ngram_list = list(zip(*all_labels_list))
    for i in range(args.n):
        temp_list = ngram_list[i]
        fw = open(args.out_prefix + '%dgram' % i)
        out_list = [' '.join(list(map(str, l))) + '\n' for l in temp_list]
        fw.writelines(out_list)
        fw.close()


if __name__ == '__main__':
    main(parse_args())
