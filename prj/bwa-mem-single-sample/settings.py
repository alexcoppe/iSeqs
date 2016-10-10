#The reference genome in fasta format
reference = "reference.fa"
referenceDir = "./genome"

#The paired reads in fastq format
reads1 = "m1_TAAGGCGA_R1_M.fastq.gz"
reads2 = "m1_TAAGGCGA_R2_M.fastq.gz"

#Annotation directory
annotationDir = "./annotation"
#Exome sequencing kit bed file
exomeRegions = "nexterarapidcapture_exome_targetedregions_v1.2.bed"

#Directory containing  GenomeAnalysisTK.jar  
gatkJarDir = "~/local/GenomeAnalysisTK/"

#The dbSNP vcf file
dbsnpVCF = "All_20151104.vcf"

#Project metadata
projectName = "m1"
sampleName = "m1"

#Computational resources
processors = 8
maxMemory = 1000000000

removeNs = "y"

removeSoftClipped = "n"
