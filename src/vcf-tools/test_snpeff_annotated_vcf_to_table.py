#!/usr/bin/env python

import unittest
import sys
from snpeff_annotated_vcf_to_table import *


class Test(unittest.TestCase):
    def setUp(self):
        self.mutect_vcf = open("../../test-data/mutect.vcf")
        self.mutect2_vcf = open("../../test-data/mutect2.vcf")

    def tearDown(self):
        self.mutect_vcf.close()
        self.mutect2_vcf.close()

    def get_first_variant_from_vcf(self, program="mutect2"):
        if program == "mutect": f = self.mutect_vcf
        if program == "mutect2": f = self.mutect2_vcf
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


    def test_build_genotype_dictionary_mutect(self):
        format_field,sample_field = self.get_format_value_for_first_sample("mutect")
        returned_value = build_genotype_dictionary(format_field,sample_field)
        d = {}
        assert returned_value.__class__ == d.__class__

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
        variant_line = self.get_first_variant_from_vcf()
        keys = sorted(["chr", "rs", "pos", "ref", "alt", "info_field", "format_field", "sample_fields"])
        returned_value = sorted(get_vcf_fixed_fields(variant_line).keys())
        self.assertListEqual(keys, returned_value)
        

    def test_number_of_sample_fields_in_mutect(self):
        variant_line = self.get_first_variant_from_vcf()
        returned_value = get_vcf_fixed_fields(variant_line)
        number_of_samples = len(returned_value.get("sample_fields"))
        self.assertEqual(number_of_samples, 2)


    def test_number_of_trascripts_from_mutect_vcf(self):
        variant_line = self.get_first_variant_from_vcf("mutect")
        transcripts = get_transcripts_from_info_field(variant_line)
        self.assertEqual(len(transcripts), 6)

    def test_number_of_trascripts_from_non_annotated_vcf(self):
        variant_line = self.get_first_variant_from_vcf("mutect2")
        transcripts = get_transcripts_from_info_field(variant_line)
        self.assertEqual(len(transcripts), 0)

    def test_first_transcript_is_dict(self):
        variant_line = self.get_first_variant_from_vcf("mutect")
        transcripts = get_transcripts_from_info_field(variant_line)
        first_transcript = transcripts[0]
        d = {}
        assert first_transcript.__class__ == d.__class__

    def test_filter_high_impact_transcripts_from_first_variant(self):
        variant_line = self.get_first_variant_from_vcf("mutect")
        transcripts = get_transcripts_from_info_field(variant_line, ["HIGH"])
        self.assertEqual(len(transcripts), 0)

    def test_filter_high_impact_transcripts_from_first_variant(self):
        variant_line = self.get_first_variant_from_vcf("mutect")
        transcripts = get_transcripts_from_info_field(variant_line, ["MODIFIER"])
        self.assertEqual(len(transcripts), 6)




if __name__ == "__main__":
    unittest.main()
