#The reference genome in fasta format
reference = "reference.fa"
referenceDir = "~/annotation/"
#referenceDir = "./genome"

#The paired reads in fastq format
reads1 = "1.fastq.gz"
reads2 = "2.fastq.gz"

##Annotation directory
annotationDir = "~/annotation/"
#Exome sequencing kit bed file
exomeRegions = "nexterarapidcapture_exome_targetedregions_v1.2.bed"

#Directory containing  GenomeAnalysisTK.jar  
gatkJarDir = "~/local/GenomeAnalysisTK/"

#Directory containing picard.jar
picardDir = "~/local"


##Project metadata
projectName = "m2"
sampleName = "m2"

##Computational resources
processors = 8
maxMemory = 1000000000

#Remove flanking Ns
removeNs = "n"


#Choose between samtools or picard
tool = "samtools"

#The dbSNP vcf file
dbsnpVCF = "All_20170710.vcf"




################################################################################################
########### Samtools parameters ################################################################
################################################################################################

#samtools -q parameter: minimum mapping quality [0]
samQuality = 0
#samtools required flag, 0 for unset [0] (for example 2)
requiredFlag = 0
#samtools filtering flag, 0 for unset [0] (for example 256)
filteringFlag = 0
