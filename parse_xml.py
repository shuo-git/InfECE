from utils import *


def label_word(line):
    words = line.split(',')
    label = words[-2]

    end1 = line.find('",', 1)
    left_word = line[1:end1]
    start2 = end1 + 3
    end2 = line.find('",', start2)
    right_word = line[start2:end2]
    assert len(line[end2+2:].split(',')) == 2
    return left_word, right_word, label


def main():
    lines = file2lines(sys.argv[1])
    num_lines = len(lines)
    label_lines = []
    text_lines = []
    temp_label_line = []
    temp_text_line = []
    prev_d = False
    idx = 0
    while idx < num_lines:
        line = lines[idx].strip()
        if not line.startswith('<'):
            lw, rw, lb = label_word(line)
            if len(rw) > 0:
                temp_text_line.append(rw)
                if prev_d:
                    temp_label_line.append('D')
                else:
                    temp_label_line.append(lb)
            if lb == 'D':
                prev_d = True
            else:
                prev_d = False
        elif line.startswith('</seg>'):
            label_lines.append(temp_label_line)
            text_lines.append(temp_text_line)
            temp_label_line = []
            temp_text_line = []
        idx += 1

    words2file(label_lines, sys.argv[2] + '.label')
    words2file(text_lines, sys.argv[2] + '.text')


if __name__ == "__main__":
    main()
