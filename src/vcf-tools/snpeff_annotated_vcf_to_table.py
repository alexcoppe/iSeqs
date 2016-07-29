#!/usr/bin/env python

import argparse
import sys


def build_format_dictionary(format_string, sample_string):
    keys = format_string.split(":")
    values = sample_string.split(":")
    return dict(zip(keys, values))
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Do something")

    parser.add_argument('-f', '--vcf', action='store', type=file, help="vcf file", required=True)
    parser.add_argument("-p", "--patient", help="Patient name to be printed in patient column", required=False, type=str, default="")
    parser.add_argument("-i", "--impacts", help="List of impacts to be filtered, separated by ,", required=False, type=str, default="")
    args = parser.parse_args()

    patient = args.patient
    impacts = args.impacts.split(",")


    variant_columns = ["chr", "pos", "rs", "ref"]
    transcript_columns = ["alt", "annotation", "impact", "gene_name", "ensg", "feature_type", "feature", "transcript_biotype", "rank", "hgvs_c", "hgvs_p", "cDNA_position", "CDS_position_CDS_len", "protein_position_protein_len", "distance_to_feature"]

    header = "\t".join(variant_columns + transcript_columns)
    if patient: header = "patient\t" + header
    print header

    for line in  args.vcf:
        if not line.startswith("#"):
            chr,pos,rs,ref,alt = line.split()[0:5]
            info_field = line.split()[7]
            format_field = line.split()[8]
            sample_field = line.split()[9]
            format_dictionary = build_format_dictionary(format_field, sample_field)

            #See http://snpeff.sourceforge.net/VCFannotationformat_v1.0.pdf for variant annotation vcf format
            annotation_field = [el for el in info_field.split(";") if el.startswith("ANN=")][0][4:]
            transcripts = annotation_field.split(",")
            for transcript in transcripts:
                splitted_transcript = transcript.split("|")


                transcript_annotation = dict(zip(transcript_columns, splitted_transcript))

                if transcript_annotation.get("impact") in impacts or impacts == [""]:
                    if patient:
                        patient_string = "{}\t".format(patient)
                    else:
                        patient_string = ""

                    variant_string = "{}\t{}\t{}\t{}\t".format(chr, pos, rs, ref)

                    print variant_string + "\t".join( ["{" + el + "}" for el in transcript_columns] ).format(**transcript_annotation)
