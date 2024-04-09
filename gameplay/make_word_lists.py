import math
import random

if __name__ == '__main__':
    with open('dictionary.txt', encoding='utf-8') as infile:
        with open('dictionary_little.txt', mode='w', encoding='utf-8') as outfile:
            in_lines = 0
            out_lines = 0
            for line in infile:
                in_lines += 1
                # ln(2)/(2ln(x)^2)
                if random.random() < math.log(2)/(math.log(len(line.strip()))**4):
                    outfile.write(f'{line}')
                    out_lines += 1
    print(f'kept {out_lines}/{in_lines} ({out_lines*100/in_lines}%)')

