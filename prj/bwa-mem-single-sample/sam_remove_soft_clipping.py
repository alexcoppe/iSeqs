#!/usr/bin/env python

import sys
import re
import argparse


def number_of_soft_clipped_bases(read):
    p = re.compile("\d+S")
    cigar = read.strip().split()[5]
    matches = p.findall(cigar)
    if len(matches) != 0:
        number_of_clipped_bases = sum( [ int(match.replace("S", "")) for match in matches] )
        return number_of_clipped_bases
    return 0


def main():
    parser = argparse.ArgumentParser(description='Remove reads with soft clipping from sam file')
    parser.add_argument("-n", "--nucleotides", type=int, help="Maximum number of allowed soft clipped nucleotides per read", default=5)
    args = parser.parse_args()

    p = re.compile("\d+S")
    while True:
        mate1 = sys.stdin.readline()
        if mate1.startswith("@"):
            sys.stdout.write(mate1)
            continue
        mate2 = sys.stdin.readline()

        if not mate1 or not mate2:
            break

        mate1_clipped_bases = number_of_soft_clipped_bases(mate1)
        mate2_clipped_bases = number_of_soft_clipped_bases(mate2)

        if mate1_clipped_bases < args.nucleotides and mate2_clipped_bases < args.nucleotides:
            sys.stdout.write(mate1)
            sys.stdout.write(mate2)


if  __name__ == "__main__":
    main()

