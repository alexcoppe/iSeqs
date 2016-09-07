#The reference genome in fasta format
reference = "reference.fa"
referenceDir = "~/genomic_data/human_genome/"

#Annotation directory
annotationDir = "~/annotation/"
#Exome sequencing kit bed file
exomeRegions = "nexterarapidcapture_exome_targetedregions_v1.2.bed"


##The dbSNP vcf file
#dbsnpVCF = "All_20151104.vcf"

##Computational resources
#processors = 8
#maxMemory = 1000000000

#The bam from the tumoreal sample
tumorBam = "ric.bam"
normalBam = "rem.bam"


startChr = 5
endChr = 6

snpeffDir = "~/local/snpEff"
snpeffGenomeVersion = "GRCh37.75"

#Clinvar vcf
clinvarVCF = "clinvar.vcf.gz"

#Cosmic vcfs
cosmicCodingVCF = "CosmicCodingMuts_v77.vcf.gz"
cosmicNonCodingVCF = "CosmicNonCodingVariants.vcf.gz"
