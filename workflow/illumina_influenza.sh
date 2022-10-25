#!/bin/bash
while getopts 's:d:' OPTION
do
	case $OPTION in 
	s ) SAMPLESHEET=$OPTARG;;
    d ) DATAPATH=$OPTARG;;
	esac
done
bpath=
if [ "$bpath" == "" ]; then
	bpath=$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
fi

[[ ! -d IRMA/ ]] && mkdir IRMA
for sample in $(cut -f1 -d, $SAMPLESHEET ); do
    docker run --rm -v $PWD:/data public.ecr.aws/n3z8t4o2/irma:1.0.2p3 IRMA FLU fastqs/*/${sample}*R1*.fastq* fastqs/*/${sample}*R2*.fastq*  IRMA/$sample |tee -a ./log.out 2> ./log.err
    done



cat IRMA/*/*.fasta > dais_input.fasta

$bpath/scripts/daiswrapper.sh -i dais_input.fasta -m INFLUENZA 

