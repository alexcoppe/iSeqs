#!/usr/bin/env python

import unittest
import sys
from vcf_2_table import *


class Test(unittest.TestCase):
    def setUp(self):
        self.mutect_vcf = open("../../test-data/mutect.vcf")
        self.mutect2_vcf = open("../../test-data/mutect2.vcf")
        self.multiple_alts = open("../../test-data/mutect-multiple.vcf")

    def tearDown(self):
        self.mutect_vcf.close()
        self.mutect2_vcf.close()
        self.multiple_alts.close()

    def get_first_variant_from_vcf(self, program="mutect2"):
        if program == "mutect": f = self.mutect_vcf
        if program == "mutect2": f = self.mutect2_vcf
        if program == "multiple": f = self.multiple_alts
        for line in f:
            if not line.startswith("#"):
                return line
        

    def get_format_value_for_first_sample(self, program="mutect"):
        if program == "mutect": f = self.mutect_vcf
        if program == "mutect2": f = self.mutect2_vcf
        for line in f:
            if not line.startswith("#"):
                splitted = line.split()
                format_field = splitted[8]
                first_sample_field = splitted[9]
                if program == "mutect2":
                    second_sample_field = splitted[10]
        return format_field,first_sample_field


    def test_build_genotype_dictionary_keys_with_mutect(self):
        format_field,sample_field = self.get_format_value_for_first_sample("mutect")
        returned_value = build_genotype_dictionary(format_field,sample_field)
        keys = sorted(returned_value.keys())
        self.assertListEqual(keys, sorted(["GT", "AD", "BQ", "DP", "FA", "SS"]))

    def test_build_genotype_dictionary_keys_with_mutect2(self):
        format_field,sample_field = self.get_format_value_for_first_sample("mutect2")
        returned_value = build_genotype_dictionary(format_field,sample_field)
        keys = sorted(returned_value.keys())
        self.assertListEqual(keys, sorted(["GT","AD","AF","ALT_F1R2","ALT_F2R1","FOXOG","QSS","REF_F1R2","REF_F2R1"]))

    def test_get_vcf_variant_fields(self):
        variant_line = self.get_first_variant_from_vcf("multiple")
        keys = sorted(["chr", "rs", "pos", "ref", "alt", "info_field", "format_field", "sample_fields"])
        returned_value = sorted(get_vcf_fixed_fields(variant_line).keys())
        self.assertListEqual(keys, returned_value)
        

    def test_number_of_sample_fields_in_mutect(self):
        variant_line = self.get_first_variant_from_vcf()
        returned_value = get_vcf_fixed_fields(variant_line)
        number_of_samples = len(returned_value.get("sample_fields"))
        self.assertEqual(number_of_samples, 2)

    def test_transcripts_by_alt_multiple_alelles(self):
        variant_line = self.get_first_variant_from_vcf("multiple")
        returned_value = split_transcripts_by_alt(get_vcf_fixed_fields(variant_line)).keys()
        l = ["T", "TA"]
        self.assertEqual(returned_value, l)

    def test_transcripts_by_alt_single_allele(self):
        variant_line = self.get_first_variant_from_vcf("mutect")
        returned_value = split_transcripts_by_alt(get_vcf_fixed_fields(variant_line)).keys()
        l = ["A"]
        self.assertEqual(returned_value, l)

    def test_transcripts_by_alt_no_transcript_annotation(self):
        variant_line = self.get_first_variant_from_vcf()
        returned_value = split_transcripts_by_alt(get_vcf_fixed_fields(variant_line)).keys()
        self.assertEqual(returned_value, [])


    def test_split_genotype_by_alt_multiple(self):
        variant_line = self.get_first_variant_from_vcf("multiple")
        returned_value = split_genotypes_by_alt(get_vcf_fixed_fields(variant_line))
        number_of_samples = len(returned_value.keys())
        self.assertEqual(number_of_samples, 2)


    def test_keys_from_split_genotype_by_alt_multiple(self):
        variant_line = self.get_first_variant_from_vcf("multiple")
        returned_value = split_genotypes_by_alt(get_vcf_fixed_fields(variant_line)).keys()
        l = ["T", "TA"]
        self.assertEqual(returned_value, l)

    def test_split_genotype_by_alt_single(self):
        variant_line = self.get_first_variant_from_vcf()
        returned_value = split_genotypes_by_alt(get_vcf_fixed_fields(variant_line))
        number_of_samples = len(returned_value.keys())
        self.assertEqual(number_of_samples, 1)


    def test_modify_alternative_allele_index0(self):
        sample_genotyp_dict = {'GT': '1/2', 'GQ': '99', 'AD': '0,8,13', 'DP': '36', 'PL': '1197,790,1238,471,0,756'}
        returned_value = modify_alternative_allele(sample_genotyp_dict, 0).get("AD")
        self.assertEqual(returned_value, "0,8")

    def test_modify_alternative_allele_index1(self):
        sample_genotyp_dict = {'GT': '1/2', 'GQ': '99', 'AD': '0,8,13', 'DP': '36', 'PL': '1197,790,1238,471,0,756'}
        returned_value = modify_alternative_allele(sample_genotyp_dict, 1).get("AD")
        self.assertEqual(returned_value, "0,13")

    def test_split_vcf_line_by_alt_multiple(self):
        variant_line = self.get_first_variant_from_vcf("multiple")
        returned_value = len(split_vcf_line_by_alt(variant_line))
        self.assertEqual(returned_value, 2)

    def test_split_vcf_line_by_alt_single(self):
        variant_line = self.get_first_variant_from_vcf()
        returned_value = len(split_vcf_line_by_alt(variant_line))
        self.assertEqual(returned_value, 1)


    def test_from_splitted_variants_to_transcripts_multiple(self):
        variant_line = self.get_first_variant_from_vcf("multiple")
        variants_in_line = split_vcf_line_by_alt(variant_line)
        returned_value = len(from_splitted_variants_to_transcripts(variants_in_line))
        self.assertEqual(returned_value, 14)

    def test_from_splitted_variants_to_transcripts_single(self):
        variant_line = self.get_first_variant_from_vcf("mutect")
        variants_in_line = split_vcf_line_by_alt(variant_line)
        returned_value = len(from_splitted_variants_to_transcripts(variants_in_line))
        self.assertEqual(returned_value, 6)

    def test_from_splitted_variants_to_transcripts_no_transcript_annotation(self):
        variant_line = self.get_first_variant_from_vcf()
        variants_in_line = split_vcf_line_by_alt(variant_line)
        returned_value = len(from_splitted_variants_to_transcripts(variants_in_line))
        self.assertEqual(returned_value, 1)


if __name__ == "__main__":
    unittest.main()
