#!/usr/bin/env python

import argparse
import sys

#VCF annotation fields. See http://snpeff.sourceforge.net/VCFannotationformat_v1.0.pdf for variant annotation vcf format
transcript_properties = ["alt", "annotation", "impact", "gene_name", "ensg", "feature_type", "feature", "transcript_biotype", "rank", "hgvs_c", "hgvs_p", "cDNA_position", "CDS_position_CDS_len", "protein_position_protein_len", "distance_to_feature"]



#Given a FORMAT field as string (e.g. GT:AD:BQ:DP:FA:SS)
#and a genotype field (e.g. 0:100,1:.:101:9.901e-03:0) both with colon-separated data
#It returns a dictionary with keys from the FORMAT field and values from the genotype field
# (e.g. {'GT': '0', 'AD': '100,1', 'SS': '0', 'FA': '9.901e-03', 'BQ': '.', 'DP': '101'}
def build_genotype_dictionary(format_string, genotype_string):
    keys = format_string.split(":")
    values = genotype_string.split(":")
    return dict(zip(keys, values))
    
def get_vcf_fixed_fields(vcf_line):
    splitted = vcf_line.split()
    fields = {}
    fields["chr"],fields["pos"],fields["rs"],fields["ref"],fields["alt"] = splitted[0:5]
    fields["info_field"] = splitted[7]
    fields["format_field"] = splitted[8]
    fields["sample_fields"] = splitted[9:]
    return fields

def get_transcripts_from_info_field(line, impacts=[""]):
    info_field = line.split()[7]
    transcripts_string = [el for el in info_field.split(";") if el.startswith("ANN=")]
    transcripts = []
    if transcripts_string == []:
        return []
    else:
        transcripts_string = transcripts_string[0][4:]
        for transcript in transcripts_string.split(","):
            splitted_transcript = transcript.split("|")
            transcript_annotation = dict(zip(transcript_properties, splitted_transcript))
            transcripts.append(transcript_annotation)
    transcripts = [transcript for transcript in transcripts if transcript.get("impact") in impacts or impacts == [""]]
    return transcripts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Do something")

    parser.add_argument('-f', '--vcf', action='store', type=file, help="vcf file", required=True)
    parser.add_argument("-p", "--patient", help="Patient name to be printed in patient column", required=False, type=str, default="")
    parser.add_argument("-i", "--impacts", help="List of impacts to be filtered, separated by ,", required=False, type=str, default="")
    args = parser.parse_args()

    patient = args.patient
    impacts = args.impacts.split(",")


    variant_columns = ["chr", "pos", "rs", "ref"]

    header = "\t".join(variant_columns + transcript_properties)
    if patient: header = "patient\t" + header

    printed_header = 0
    for line in  args.vcf:
        if not line.startswith("#"):
            variant_fields = get_vcf_fixed_fields(line)
            format_field = variant_fields.get("format_field")
            sample_fields = variant_fields.get("sample_fields")

            sample_index = 1
            sample_columns = []
            for sample in sample_fields:
                format_dictionary =  build_genotype_dictionary(format_field, sample_fields[0])
                format_keys = format_dictionary.keys()
                sample_string = "\t".join(["{" + el + "}" for el in format_keys]).format(**format_dictionary)
                sample_columns.append(sample_string)
                header = header + "\tsample{}_".format(sample_index) + "\tsample{}_".format(sample_index).join(format_keys)
                sample_index += 1
            samples_string = "\t".join(sample_columns)


            transcripts = get_transcripts_from_info_field(line)
            variant_string = "{chr}\t{pos}\t{rs}\t{ref}".format(**variant_fields)

            if not printed_header:
                print header
                printed_header = 1

            #If the VCF has not been annotated with SnpEff
            if not transcripts:
                variant_columns = ["chr", "pos", "rs", "ref", "alt"]
                total_columns = len(variant_columns + transcript_properties[1:])
                variant_string = "{chr}\t{pos}\t{rs}\t{ref}\t{alt}".format(**variant_fields)
                print variant_string + "\t" + "\t".join(["NA"] * (len(transcript_properties) -1) ) + "\t" + samples_string
            #If the VCF has been annotated with SnpEff
            else:
                for transcript in transcripts:
                    transcript_string = "\t".join( ["{" + el + "}" for el in transcript_properties] ).format(**transcript)
                    print "\t".join([variant_string, transcript_string, samples_string])

