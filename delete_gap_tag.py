from utils import *


lines = file2words(sys.argv[1])
res_lines = [line[1::2] for line in lines]
words2file(res_lines, sys.argv[2])
