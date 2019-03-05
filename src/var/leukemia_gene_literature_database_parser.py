#!/usr/bin/env python


"""leukemia_gene_literature_database_parser.py: Parses the Leukemia Gene Literature
   Database and returns GeneSymbols and Aliases"""

__author__      = "Alessandro Coppe"
__copyright__   = "WTFPL"
__version__     = "0.1 alpha"


import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Parses the Leukemia Gene Literature Database and returns GeneSymbols and Aliases")
    parser.add_argument("-i","--input", help = "Input file from LGL Database", required = True)
    parser.add_argument("-o","--output", help = "Type of output (default byline, possibilities: byline)", required = False, default = "byline")
    args = parser.parse_args()

    lglGeneSymbolsAndAliases = []

    inputFile = args.input

    try:
        with open(inputFile) as lglFile:
            data = lglFile.readlines()
    except:
        sys.stderr.write("Could not open file {}\n".format(inputFile))
        sys.exit(1)

    lineNumber = 0
    for line in data:
        if lineNumber == 0:
            lineNumber += 1
        else:
            splittedLine = line.split()
            geneSymbol = splittedLine[1]
            lglGeneSymbolsAndAliases.append(geneSymbol)
            aliases = splittedLine[2].split("|")
            if "-" in aliases:
                pass
            else:
                lglGeneSymbolsAndAliases + aliases

    if args.output == "byline":
        for gene in lglGeneSymbolsAndAliases:
            print gene
    else:
        sys.stderr.write("Not supported {} as type of output\n".format(args.output))
        sys.exit(1)

if  __name__ == "__main__":
    main()

