import numpy as np
import argparse

from utils import *


def parse_args():
    parser = argparse.ArgumentParser(description="Calculate inference ECE")
    parser.add_argument("--prob", default="prob.txt")
    parser.add_argument("--trans", default="trans.txt")
    parser.add_argument("--label", default="label.txt")
    parser.add_argument("--vocabulary", default="vocab.en.txt")
    parser.add_argument("--bins", type=int, default=20)

    return parser.parse_args()


def error_matrix(prob_list, token_list, label_list, vocab, **kwargs):
    """
    :param prob_list: list
    :param token_list: list
    :param label_list: list
    :param vocab: dict, map str to int
    :return:
    """
    assert len(prob_list) == len(token_list)
    assert len(prob_list) == len(label_list)

    token_idx_list = lookup_vocab4line(token_list, vocab)
    vocab_size = len(vocab)

    prob_array = np.array(prob_list)
    label_array = np.array(label_list)
    token_idx_array = np.array(token_idx_list)
    value_array = label_array - prob_array

    bins = kwargs.get("bins") or 20
    bin_width = 1.0 / bins
    list_len = len(prob_list)
    err_matrix = np.zeros((bins, vocab_size))
    count_matrix = np.zeros((bins, vocab_size))
    prob_matrix = np.zeros((bins, vocab_size))
    for i in range(bins):
        lower_bound = i * bin_width
        upper_bound = (i + 1) * bin_width
        if i < bins - 1:
            cond = (prob_array >= lower_bound) & (prob_array < upper_bound)
        else:
            cond = (prob_array >= lower_bound) & (prob_array <= upper_bound)
        for j in range(list_len):
            if cond[j]:
                err_matrix[i][token_idx_array[j]] += value_array[j]
                prob_matrix[i][token_idx_array[j]] += prob_array[j]
                count_matrix[i][token_idx_array[j]] += 1

    assert list_len == np.sum(count_matrix)

    return err_matrix, prob_matrix, count_matrix


def calculate_ece(emtrx, cmtrx):
    return np.sum(np.abs(np.sum(emtrx, axis=1))) / np.sum(cmtrx)


def calculate_token_ece(emtrx, cmtrx):
    return np.sum(np.abs(emtrx)) / np.sum(cmtrx)


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

    err_mtrx, prob_mtrx, count_mtrx = error_matrix(prob,
                                                   trans,
                                                   float_label, vocab, bins=args.bins)

    infece = calculate_ece(err_mtrx, count_mtrx)
    token_ece = calculate_token_ece(err_mtrx, count_mtrx)

    print("{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}".format(infece, token_ece, np.mean(prob), np.mean(float_label)))


if __name__ == '__main__':
    main(parse_args())
