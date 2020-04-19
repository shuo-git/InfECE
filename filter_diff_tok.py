import utils as utils
import sys


def del_end_blk(lines):
    if len(lines[-1]) == 0:
        del lines[-1]
    return lines


def main():
    cmplines1 = utils.file2words(sys.argv[1])           # Original Hyp
    cmplines2 = utils.file2words(sys.argv[2])           # Shift Back of Shifted Hyp
    trglines = utils.file2words(sys.argv[3])            # File to be Filtered
    del_end_blk(cmplines1)
    del_end_blk(cmplines2)
    del_end_blk(trglines)
    reslines = []
    num_line = len(trglines)

    assert len(cmplines1) == num_line
    assert len(cmplines2) == num_line

    num_filt = 0
    num_total = 0
    for i in range(num_line):
        temp_line = []
        num_word = len(trglines[i])

        assert len(cmplines1[i]) == num_word
        assert len(cmplines2[i]) == num_word

        num_total += num_word
        for j in range(num_word):
            if cmplines1[i][j] == cmplines2[i][j] or '?' in cmplines2[i][j]:
                temp_line.append(trglines[i][j])
            else:
                num_filt += 1
        reslines.append(temp_line)

    utils.words2file(reslines, sys.argv[3]+'.filt')
    print("Total: %d" % num_total)
    print("Filtered: %d \t %f" % (num_filt, 1.0*num_filt/num_total))


if __name__ == "__main__":
    main()
