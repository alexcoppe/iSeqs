#!/bin/bash

echo -n "Are you sure you want to remove all intermediate files (y/n)? "

read yes

if [ "$yes" == "y" ]; then
    rm -f *.pyc *.grp mapping.bam mapping-sorted.bam mapping-sorted-rmdup.bam  mapping-sorted-rmdup.bam.bai  mapping-sorted-rmdup-realigned.bai mapping-sorted-rmdup-realigned.bam realigning.intervals
    exit 1
else
    exit 1
fi
