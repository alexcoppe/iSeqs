#!/usr/bin/env python

import argparse
import sys
import vcf


def is_heterozygous(record):
    sample = record.samples[0]
    genotype = sample['GT']
    alleles = genotype.split("/")
    if "2" in alleles:
        return False
    if len(alleles) > 2:
        return False
    if len(alleles) == 1:
        return False
    if len(set(alleles)) == 1:
        return False
    return True

def get_allele_freqs(record):
    sample = record.samples[0]
    read_depth = sample['DP']
    allele1_depth,allele2_depth = sample["AD"]
    if read_depth == 0:
        return [float("inf"), float("inf")]
    return [float(allele1_depth) / read_depth, float(allele2_depth) / read_depth]
    

def filter_record_by_genotype_qual(record, qual=60):
    sample = record.samples[0]
    try:
        gq = sample["GQ"]
    except:
        return False
    if gq > qual:
        return True
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="From tumor-normal matched samples vcfs, builds a tsv with normal and tumor allele frequences of heterozygous germline calls")
    parser.add_argument('-n', '--normal', action='store', type=str, help="Normal sample vcf", required=True)
    parser.add_argument('-t', '--tumor', action='store', type=str, help="Tumor sample vcf", required=True)
    parser.add_argument('-q', '--quality', action='store', type=int, help="Genotype call quality filter", required=False, default=60)
    args = parser.parse_args()

    normal_heterozygous_variants = {}

    with open(args.normal) as f:
        vcf_reader = vcf.Reader(f)
        for record in vcf_reader:
            if is_heterozygous(record):
                if record.FILTER == [] or record.FILTER == None:
                    if filter_record_by_genotype_qual(record, args.quality):
                        pos = record.POS
                        ref = record.REF
                        alt = record.ALT
                        key = "{},{},{}".format(pos,ref,alt)
                        normal_heterozygous_variants[key] = record

    with open(args.tumor) as f:
        vcf_reader = vcf.Reader(f)
        for record in vcf_reader:
            if record.FILTER == [] or record.FILTER == None:
                if filter_record_by_genotype_qual(record, args.quality):
                    pos = record.POS
                    ref = record.REF
                    alt = record.ALT
                    key = "{},{},{}".format(pos,ref,alt)
                    normal = normal_heterozygous_variants.get(key)
                    if normal:
                        normal_allele_freq = get_allele_freqs(normal)[1]
                        tumor_allele_freq = get_allele_freqs(record)[1]
                        if tumor_allele_freq == float("inf")  or normal_allele_freq == float("inf"):
                            pass
                        print "{}\t{}\t{}\t{}\t{}\t{}".format(record.CHROM, record.POS, record.REF, record.ALT[0], tumor_allele_freq,  normal_allele_freq )
