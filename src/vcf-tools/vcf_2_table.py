#!/usr/bin/env python

import argparse
import sys

#VCF annotation fields. See http://snpeff.sourceforge.net/VCFannotationformat_v1.0.pdf for variant annotation vcf format
transcript_properties = ["alt", "annotation", "impact", "gene_name", "ensg", "feature_type", "feature", "transcript_biotype", "rank", "hgvs_c", "hgvs_p", "cDNA_position", "CDS_position_CDS_len", "protein_position_protein_len", "distance_to_feature"]


#Given a sample genotype dictionary like: {'GT': '1/2', 'GQ': '99', 'AD': '0,8,13', 'DP': '36', 'PL': '1197,790,1238,471,0,756'}
#modifies the AD value keeping only the depth of coverage for only one alternative allele indicated by alt_index
#For example: for alt_index 0 (first alternative allele) will return:
#{'GT': '1/2', 'GQ': '99', 'AD': '0,8', 'DP': '36', 'PL': '1197,790,1238,471,0,756'}
def modify_alternative_allele(sample_genotype_dictionary, alt_index):
    alt_index += 1
    ad = sample_genotype_dictionary.get("AD")
    splitted_allele_count = ad.split(",")
    ref = splitted_allele_count[0]
    alt = splitted_allele_count[alt_index]
    ad_value = ",".join([ref,alt])
    d = dict(sample_genotype_dictionary)
    d["AD"] = ad_value
    return d


#Takes as input a dictionary obtained by splitting a vcf data line in different fields.
#Keys are: ['format_field', 'rs', 'pos', 'chr', 'sample_fields', 'alt', 'info_field', 'ref'] 
#values are the splitted strings from the vcf
#
#Returns a dictionary with keys being the  alternative alleles in the genomic position (e.g. ["A", "T"]
#The values are a list of dictionaries. Each dictionary is build up from vcf's sample field:
#[ {'FA': '9.901e-03', 'GT': '0', 'AD': '100,1', 'SS': '0', 'DP': '101', 'BQ': '.'} ] 
#The upper example is from a single sample vcf
def split_genotypes_by_alt(variant_fields):
    d = {}
    alts = variant_fields.get("alt").split(",")
    format_field = variant_fields.get("format_field")
    sample_fields = variant_fields.get("sample_fields")
    alt_index = 0
    for alt in alts:
        samples_dict = []
        for sample in sample_fields:
            original_sample_dict = build_genotype_dictionary(format_field, sample)
            new_sample_dict = modify_alternative_allele(original_sample_dict, alt_index)
            samples_dict.append(new_sample_dict)
            ad = original_sample_dict.get("AD")
        alt_index += 1
        d[alt] = samples_dict
    return d


#Split transcripts affected by variant based on the alternative allele. Multiple alternative alleles
#are in the same line in vcfs, in such a case, this function splits transcript annotations, like impact, based
#on alternatvie allele.
#Takes as input a dictionary obtained by splitting a vcf data line in different fields.
#Keys are: ['format_field', 'rs', 'pos', 'chr', 'sample_fields', 'alt', 'info_field', 'ref'] 
#values are the splitted strings from the vcf
#
#Returns a dictionary with keys being the  alternative alleles present at the genomic position (e.g. ["A", "T"]
#values of the returned dictionary are lists of dictionaries. Each dictionary contains information 
#obtained by parsing the EFF=subfield from the INFO field of the vcf
#If if the vcf has no EFF subfield an empty dictionary is returned
def split_transcripts_by_alt(variant_fields):
    d = {}
    info_field = variant_fields.get("info_field")
    transcripts_string = [el for el in info_field.split(";") if el.startswith("ANN=")]
    transcripts = []
    if transcripts_string == []:
        return {}
    else:
        transcripts_string = transcripts_string[0][4:]
        for transcript in transcripts_string.split(","):
            splitted_transcript = transcript.split("|")
            transcript_annotation = dict(zip(transcript_properties, splitted_transcript))
            alt = transcript_annotation.get("alt")
            d.setdefault(alt, [])
            d[alt].append(transcript_annotation)
    return d

#Takes as input a data line from a vcf, it returns a list of dictionaries.
#The length of the returned list equals the number of alternative alleles in the genomic position
#and each element of the list is a dictionary with data about the variants. These dictionaries are
#identical to the one obtained by get_vcf_fixed_fields with the alt field having a single alternative allele in case
#of multiple alts in the considered position and two new keys:
# - transcripts: a list of trascript annotations (dictionaries) with a single alt
# - samples: a list of sample annotaions (dictionaries) with a single alt
def split_vcf_line_by_alt(line):
    variant_fields = get_vcf_fixed_fields(line)
    #A dict like {'C': [{'FA': '0.00', 'GT': '0', 'AD': '19,0', 'SS': '0', 'DP': '19', 'BQ': '.'}]}
    samples_by_alt = split_genotypes_by_alt(variant_fields)
    transcripts_by_alt = split_transcripts_by_alt(variant_fields)
    variants = []
    for alt in samples_by_alt.keys():
        variant = dict(variant_fields)
        variant["alt"] = alt
        if transcripts_by_alt.keys() == []:
            variant["transcripts"] = []
            variant["samples"] = samples_by_alt.get(alt)
            variants.append(variant)
        else:
            variant["transcripts"] = transcripts_by_alt.get(alt)
            variant["samples"] = samples_by_alt.get(alt)
            variants.append(variant)
    return variants

#Given a list of variants in one vcf line,  obtained by split_vcf_line_by_alt function
#returns a list of dictionaries representing 
#the transcripts affected by the differente alternative alleles. The length of the returned list
#is given by (number of alternative allelele in genomic position) x (number of transcripts overlapping the genomic position)
def from_splitted_variants_to_transcripts(variants):
    transcripts_affected_by_variant = []
    variant_fields_to_drop = ["transcripts", "info_field", "format_field", "sample_fields", "samples"]
    for variant in variants:
        transcripts = variant.get("transcripts")
        samples = variant.get("samples")
        variant_data = dict(variant)
        [variant_data.pop(field, None) for field in variant_fields_to_drop]
        #If it is not annotated with SnpEff
        if transcripts == []:
            transcript_with_variant = {"transcript":None, "variant":variant_data, "samples":samples}
            transcripts_affected_by_variant.append(transcript_with_variant)
        else:
            for transcript in transcripts:
                transcript_with_variant = {"transcript":transcript, "variant":variant_data, "samples":samples}
                transcripts_affected_by_variant.append(transcript_with_variant)
    return transcripts_affected_by_variant
 


def getStuff(d,k):
    if d == None:
        return None
    if isinstance(d, list):
        return [el.get(k) for el in d]
    return d.get(k)

#Print tabulated version of from_splitted_variants_to_transcripts function
def print_transcripts(transcripts, fields = ["variant:chr", "variant:pos", "variant:ref",  "samples:AD", "samples:DP"], patient="", impacts=""):
    lines_to_print = []
    for transcript in transcripts:
        if patient:
            stuff_to_print_original_type = [patient] + [reduce(getStuff, field.split(":"), transcript) for field in fields ]
        else:
            stuff_to_print_original_type = [reduce(getStuff, field.split(":"), transcript) for field in fields ]

        if transcript.get("transcript"):
            impact = transcript.get("transcript").get("impact")
        else:
            impact = "NA"
        if impact in impacts or impacts == [""]:
            print "\t".join([str(el) if not isinstance(el, list) else "\t".join([str(subel) for subel in el]) for el in stuff_to_print_original_type])
        

def list_fields(transcripts):
    print "Available fields and subfields are:"
    transcript = transcripts[0]
    first_level_fields = transcript.keys()
    for field in first_level_fields:
        second_level_keys = transcript.get(field)
        if second_level_keys:
            print "{}".format(field)
            for second_level_field in  second_level_keys:
                if second_level_field.__class__ == {}.__class__:
                    for k in second_level_field.keys():
                        print "  - :{}".format(k)
                else:
                    print "  - :{}".format(second_level_field)
    print "Use -e \"field:subfield,field:subfield\" (e.g. \"variant:chr,variant:pos\") \" to specify with subfields to display"


#Given a FORMAT field as string (e.g. GT:AD:BQ:DP:FA:SS)
#and a genotype field (e.g. 0:100,1:.:101:9.901e-03:0) both with colon-separated data
#It returns a dictionary with keys from the FORMAT field and values from the genotype field
# (e.g. {'GT': '0', 'AD': '100,1', 'SS': '0', 'FA': '9.901e-03', 'BQ': '.', 'DP': '101'}
def build_genotype_dictionary(format_string, genotype_string):
    keys = format_string.split(":")
    values = genotype_string.split(":")
    return dict(zip(keys, values))
    
#Given a data line in a vcf, returns a dictionary with the different fields
#keys in the returned dictionary are:
#['format_field', 'rs', 'pos', 'chr', 'sample_fields', 'alt', 'info_field', 'ref'] 
def get_vcf_fixed_fields(vcf_line):
    splitted = vcf_line.split()
    fields = {}
    fields["chr"],fields["pos"],fields["rs"],fields["ref"],fields["alt"] = splitted[0:5]
    fields["info_field"] = splitted[7]
    fields["format_field"] = splitted[8]
    fields["sample_fields"] = splitted[9:]
    return fields


def print_header(vcf, fields, patient=""):
    for line in vcf:
        if not line.startswith("#"):
            variant_fields = get_vcf_fixed_fields(line)
            number_of_samples = len( variant_fields.get("sample_fields") )
            break
    header = []
    if patient:
        header.append("Patient")
    for field_subfield in fields:
        field,subfield = field_subfield.split(":")
        if field == "samples":
            samples = range(1, number_of_samples + 1)
            [header.append("{}_{}".format(s,subfield) ) for s in samples]
        else:
            header.append(subfield)
    header = "\t".join(header)
    vcf.seek(0)
    print header



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Do something")

    parser.add_argument('-f', '--vcf', action='store', type=file, help="vcf file", required=True)
    parser.add_argument("-p", "--patient", help="Patient name to be printed in patient column. If not specified, no patient column will be shown", required=False, type=str, default="")
    parser.add_argument("-i", "--impacts", help="List of impacts to be filtered, separated by ,", required=False, type=str, default="")
    parser.add_argument("-e", "--fields", help="Fields from the vcf to be printed. Use -l option to list the available fields. Fields should be specified as \"field:subfield,field:subfield:.....\"", required=False, type=str, default="")
    parser.add_argument("-l", "--list", help="List available fields to print. To use in combination with the -f option to inspect the fields and subfields available in the vcf", required=False, action="store_true")
    parser.add_argument("-H", "--header", help="Display header line", required=False, action="store_true")

    args = parser.parse_args()

    patient = args.patient
    impacts = args.impacts.split(",")
    list_fields_option = args.list

    
    if args.fields:
        fields = args.fields.split(",")
    else:
        fields = ["variant:chr", "variant:pos", "variant:ref",  "variant:alt" , "transcript:impact", "samples:AD", "samples:DP", "transcript:gene_name", "transcript:feature"]


    if not list_fields_option and args.header:
        print_header(args.vcf, fields, patient=args.patient)

    for line in  args.vcf:
        if not line.startswith("#"):
            variants_in_line = split_vcf_line_by_alt(line)
            transcripts_with_variants = from_splitted_variants_to_transcripts(variants_in_line)
            if list_fields_option:
                list_fields(transcripts_with_variants)
                sys.exit()

            print_transcripts(transcripts_with_variants, fields, patient=args.patient, impacts=impacts)
