# SCons bioinformatics pipelines
A bunch of pipelines built using SCons.

* [mutect](https://github.com/alexcoppe/iSeqs/tree/master/prj/mutect): identification of somatic variants using [MuTect](https://www.broadinstitute.org/cancer/cga/mutect)

* [docker-mutect2](https://github.com/alexcoppe/iSeqs/tree/master/prj/docker-mutect2): identification of somatic variants using a dockerized [MuTect 2](https://software.broadinstitute.org/gatk/gatkdocs/org_broadinstitute_gatk_tools_walkers_cancer_m2_MuTect2.php)

* [bwa-mem-single-sample](https://github.com/alexcoppe/iSeqs/tree/master/prj/bwa-mem-single-sample): single sample exome sequencing Illumina reads mapping using [bwa mem](http://bio-bwa.sourceforge.net).

* [mutect2-split-chr](https://github.com/alexcoppe/iSeqs/tree/master/prj/mutect2-split-chr): Somatic variants identification with [MuTect 2](https://software.broadinstitute.org/gatk/gatkdocs/org_broadinstitute_gatk_tools_walkers_cancer_m2_MuTect2.php), bam splitted by chromosome to parallelize Mutect 2 phase
