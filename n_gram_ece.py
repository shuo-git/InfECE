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
    parser.add_argument("--prob", default="prob.txt")
    parser.add_argument("--bins", type=int, default=20)
    parser.add_argument("--partition", default="uniform")

    return parser.parse_args()


def label_n_gram(reference, hypothesis, n):
    ref_n_grams = Counter(ngrams(reference, n)) if len(reference) >= n else Counter()

    labels = []
    for i in range(0, len(hypothesis) - n + 1):
        pattern = tuple(hypothesis[i:i + n])
        if ref_n_grams[pattern] > 0:
            labels.append(1)
            ref_n_grams[pattern] -= 1
        else:
            labels.append(0)
    return labels


def label_sentence(reference, hypothesis, n):
    labels_list = []
    for i in range(1, n + 1):
        labels_list.append(label_n_gram(reference, hypothesis, i))
    return labels_list


def ngram_prob(probs, n):
    res_list = []
    for line in probs:
        res_list.append([])
        llen = len(line)
        if llen < n:
            continue
        cur_value = np.sum(line[:n])
        res_list[-1].append(np.exp(cur_value))
        for j in range(n, llen):
            cur_value += line[j]
            cur_value -= line[j - n]
            res_list[-1].append(np.exp(cur_value))
    return res_list


def main(args):
    hyps = file2words(args.hyp)
    refs = file2words(args.ref)
    probs = file2words(args.prob)
    probs = [[float(x) for x in l] for l in probs]
    # probs = [[np.exp(float(x)) for x in l] for l in probs]
    all_labels_list = []
    for hyp, ref in zip(hyps, refs):
        labels_list = label_sentence(ref, hyp, 4)
        all_labels_list.append(labels_list)
    ngram_list = list(zip(*all_labels_list))
    abs_ece = []
    rel_ece = []
    sharp = []
    avg_prob = []
    multigram_label_list = []
    multigram_prob_list = []
    for i in range(4):
        label_list = ngram_list[i]
        label_list = list(itertools.chain(*label_list))
        multigram_label_list.extend(label_list)
        prob_list = ngram_prob(probs, i + 1)
        prob_list = list(itertools.chain(*prob_list))
        multigram_prob_list.extend(prob_list)
        err_vec, hit_vec, _, cnt_vec = error_vector_uniform(prob_list, label_list, bins=args.bins)
        abs_ece.append(calculate_ece(err_vec, cnt_vec) * 100)
        rel_ece.append(np.sqrt(calculate_sharpness(err_vec, cnt_vec)) * 100)
        sharp.append(np.sqrt(calculate_sharpness(hit_vec, cnt_vec)) * 100)
        avg_prob.append(np.mean(prob_list))

    err_vec, hit_vec, _, cnt_vec = error_vector_uniform(multigram_prob_list, multigram_label_list, bins=args.bins)
    abs_ece.append(calculate_ece(err_vec, cnt_vec) * 100)
    rel_ece.append(np.sqrt(calculate_sharpness(err_vec, cnt_vec)) * 100)
    sharp.append(np.sqrt(calculate_sharpness(hit_vec, cnt_vec)) * 100)
    avg_prob.append(np.mean(multigram_prob_list))

    # aggregate_abs_ece1 = np.mean(abs_ece)
    # aggregate_abs_ece2 = np.exp(np.mean(np.log(abs_ece)))
    # abs_ece.append(aggregate_abs_ece1)
    # abs_ece.append(aggregate_abs_ece2)
    #
    # aggregate_rel_ece1 = np.mean(rel_ece)
    # aggregate_rel_ece2 = np.exp(np.mean(np.log(rel_ece)))
    # rel_ece.append(aggregate_rel_ece1)
    # rel_ece.append(aggregate_rel_ece2)
    #
    # aggregate_sharp1 = np.mean(sharp)
    # aggregate_sharp2 = np.exp(np.mean(np.log(sharp)))
    # sharp.append(aggregate_sharp1)
    # sharp.append(aggregate_sharp2)
    #
    # aggregate_avg_prob1 = np.mean(avg_prob)
    # aggregate_avg_prob2 = np.exp(np.mean(np.log(avg_prob)))
    # avg_prob.append(aggregate_avg_prob1)
    # avg_prob.append(aggregate_avg_prob2)

    # abs_ece = ['{:.2f}'.format(s) for s in abs_ece]
    # rel_ece = ['{:.2f}'.format(s) for s in rel_ece]
    # sharp = ['{:.2f}'.format(s) for s in sharp]
    # avg_prob = ['{:.4f}'.format(s) for s in avg_prob]
    print('{:.2f}'.format(abs_ece[-1]))
    # print(' '.join(abs_ece) + '\t' + ' '.join(rel_ece) + '\t' + ' '.join(sharp) + '\t' + ' '.join(avg_prob))


if __name__ == '__main__':
    main(parse_args())
