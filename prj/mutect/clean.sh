#!/bin/bash

echo -n "Are you sure you want to remove all intermediate files (y/n)? "

read yes

if [ "$yes" == "y" ]; then
    rm -f mutect-confident-somatic-variants-with-eff-clinvar.vcf mutect-confident-somatic-variants-with-eff.vcf mutect-confident-somatic-variants.vcf mutect-variants.vcf.idx *.pyc
    exit 1
else
    exit 1
fi
