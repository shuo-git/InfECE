import sys
import itertools


def file2lines(filename):
    with open(filename, 'r') as fr:
        lines = fr.readlines()

    return lines


def lines2file(lines, filename):
    with open(filename, 'w') as fw:
        fw.writelines(lines)


def file2words(filename, chain=False):
    with open(filename, 'r') as fr:
        lines = fr.readlines()
        lines = list(map(lambda x: x.split(), lines))
        if chain:
            lines = list(itertools.chain(*lines))
    return lines


def words2file(lines, filename):
    lines = [' '.join(l) + '\n' for l in lines]
    lines2file(lines, filename)


def add_seg_id(lines):
    """
    :param lines: list
    :return: list
    """
    res_lines = []
    for idx, line in enumerate(lines):
        res_lines.append(line.strip() + '  (' + str(idx) + ')\n')

    return res_lines


def add_eos(lines):
    """
    :param lines: list
    :return: list
    """
    res_lines = []
    for idx, line in enumerate(lines):
        res_lines.append(line.strip() + ' <eos>\n')

    return res_lines


def load_vocab(filename, freq=False):
    words = file2lines(filename)
    vocab = {}
    if freq:
        for word in words:
            w, f = word.split()
            f = int(f)
            vocab[w] = f
    else:
        for word in words:
            w = word.split()[0]
            vocab[w] = len(vocab)

    return vocab


def lookup_vocab4line(textline, vocab):
    return [vocab[x] for x in textline]


def lookup_vocab4lines(textlines, vocab):
    """
    :param textlines: [['I', 'like', 'music', '.'], ['Hello', '!']]
    :param vocab: {'I': 1, 'like': 2, ...}
    :return: list of list
    """
    res_list = []
    for l in textlines:
        res_list.append(lookup_vocab4line(l, vocab))
    return res_list
