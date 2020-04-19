from utils import *


def exact_shift(infos):
    """
    :param infos: list of line(str)
    :return: [[start_idx, en_idx(included), shift_destination_idx-1], ...]
    """
    s_idx = 0
    e_idx = 0
    for idx, info in enumerate(infos):
        if info.startswith('NumShifts: '):
            s_idx = idx + 1
        elif info.startswith('Score: '):
            e_idx = idx
    shift_infos = infos[s_idx:e_idx]
    res_lines = []
    for line in shift_infos:
        line = line.split()
        temp_line = [int(line[0][1:-1]), int(line[1][:-1]), int(line[2].split('/')[1][:-1])]
        res_lines.append(temp_line)
    return res_lines


def extract_shifts(filename):
    lines = file2lines(filename)
    sen_shifts = []
    temp_sen = []
    for line in lines:
        if line.startswith('Sentence ID:'):
            sen_shifts.append(temp_sen)
            temp_sen = [line]
        else:
            temp_sen.append(line)
    del sen_shifts[0]
    sen_shifts.append(temp_sen)
    sen_shifts = list(map(exact_shift, sen_shifts))
    return sen_shifts


def shift_back_one_sen(tline, lline, shifts):
    shifts.reverse()
    for sft in shifts:
        left = sft[0]
        right = sft[1]
        dst = sft[2]
        length = right - left + 1
        if dst < left:
            pass
        elif dst > right:
            dst -= length
        else:
            continue

        bak_t = tline[dst+1:dst+length+1]
        bak_l = lline[dst+1:dst+length+1]
        del tline[dst+1:dst+length+1]
        del lline[dst+1:dst+length+1]

        tline[left:left] = bak_t
        lline[left:left] = bak_l
    return tline, lline


def main():
    text_lines = file2words(sys.argv[1])            # shifted text file
    label_lines = file2words(sys.argv[2])           # shifted label file
    sen_shifts = extract_shifts(sys.argv[3])        # pra file
    num_sen = len(text_lines)
    assert len(label_lines) == num_sen
    assert len(sen_shifts) == num_sen
    sb_text_lines = []
    sb_label_lines = []
    for i in range(num_sen):
        tl, ll = shift_back_one_sen(text_lines[i], label_lines[i], sen_shifts[i])
        sb_text_lines.append(tl)
        sb_label_lines.append(ll)
    words2file(sb_text_lines, sys.argv[1] + '.sb')
    words2file(sb_label_lines, sys.argv[2] + '.sb')


if __name__ == "__main__":
    main()
