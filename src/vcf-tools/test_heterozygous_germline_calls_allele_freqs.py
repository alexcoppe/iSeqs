#!/usr/bin/env python

import unittest
import sys
from heterozygous_germline_calls_allele_freqs import *
import vcf
import numpy.testing


class Test(unittest.TestCase):
    def setUp(self):
        self.mutect_vcf = open("../../test-data/mutect.vcf")
        self.mutect2_vcf = open("../../test-data/mutect2.vcf")
        self.multiple_alts = open("../../test-data/mutect-multiple.vcf")
        self.normal = open("../../test-data/normal.vcf")

    def tearDown(self):
        self.mutect_vcf.close()
        self.mutect2_vcf.close()
        self.multiple_alts.close()

    def get_n_variant_from_vcf(self, program="mutect2", n=1):
        if program == "mutect": f = self.mutect_vcf
        if program == "mutect2": f = self.mutect2_vcf
        if program == "multiple": f = self.multiple_alts
        if program == "normal": f = self.normal
        vcf_reader = vcf.Reader(f)
        record_number = 1
        for record in vcf_reader:
            if record_number == n:
                return record


    def test_first_mutect_variant_is_heterozygous(self):
        record = self.get_n_variant_from_vcf("mutect", 1)
        self.assertFalse(is_heterozygous(record))

    def test_first_normal_variant_is_heterozygous(self):
        record = self.get_n_variant_from_vcf("normal", 1)
        self.assertTrue(is_heterozygous(record))

    def test_first_normal_variant_freq(self):
        record = self.get_n_variant_from_vcf("normal", 1)
        numpy.testing.assert_almost_equal(get_allele_freqs(record), [0.5, 0.5], decimal=2)

    def test_filter_record_by_genotype_qual_with_first_normal_variant(self):
        record = self.get_n_variant_from_vcf("normal", 1)
        return_value = filter_record_by_genotype_qual(record)
        self.assertTrue(return_value)

    def test_filter_record_by_genotype_qual_very_stringent(self):
        record = self.get_n_variant_from_vcf("normal", 1)
        return_value = filter_record_by_genotype_qual(record, 100)
        self.assertFalse(return_value)


if __name__ == "__main__":
    unittest.main()
