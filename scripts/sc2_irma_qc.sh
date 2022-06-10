#!/bin/bash
#KA Lacek
#quick and dirty joint qc metric generation for a set of IRMA outputs

DIRECTORY=$1	#path to directory of irma directories
OUTFI=$2	#file to write comma-separated results
CHEMISTRY=$3	#if ONT, optional parameter to check for barcodes in config yaml 
SPIKE=$4	#if spike-only sequencing, updates the denominator for sequence proportions assembled

if [[ ${#DIRECTORY} < 1 ]];then
	echo "USAGE: sc2_irma_qc.sh <DIRECTORY HOLDING IRMA OUTPUT DIRECTORIES> <PATH TO OUTPUT CSV> (OPTIONAL: \"ONT\" IF NANOPORE SNAKEMAKE) (OPTIONAL: \"spike\" IF S-GENE ONLY SEQUENCING"
	exit 0
fi	

cd $DIRECTORY
OUTPUT=''
if [[ "ONT" == $CHEMISTRY ]]; then
	OUTPUT+="BARCODE,"
fi
OUTPUT+="SAMPLE,INITIAL_READS,QC_READS,MAPPED_READS,PERCENT_READS_MAPPED,PERCENT_COV_ASSEMBLED,COV_BASES,COV_LENGTH,AVERAGE_DEPTH\n"
for sample in $(ls -d */ | cut -f1 -d/); do

	if [[ "ONT" == $CHEMISTRY ]];then
		BARCODE=$(grep -A3 $sample ../config.yaml | grep barcode_number | cut -f6 -d ' ')
		OUTPUT+="${BARCODE},"
	fi
	OUTPUT+=$sample
	OUTPUT+=','
	[ -f $sample/tables/READ_COUNTS.txt ] && INITIAL=$(grep initial $sample/tables/READ_COUNTS.txt | cut -f2) || INITIAL=0
	OUTPUT+="${INITIAL},"
	[ -f $sample/tables/READ_COUNTS.txt ] && PASS=$(grep pass $sample/tables/READ_COUNTS.txt | cut -f2) || PASS=0
	OUTPUT+="${PASS},"
        [ -f $sample/tables/READ_COUNTS.txt ] && ALIGNED=$(grep SARS $sample/tables/READ_COUNTS.txt | cut -f2) || ALIGNED=0
	if [[ $( [ -f $sample/tables/READ_COUNTS.txt ] && grep -c SARS $sample/tables/READ_COUNTS.txt) < 1 ]];then
		ALIGNED=0
	fi
	OUTPUT+="${ALIGNED},"
	if [[ $ALIGNED -gt 0 ]]; then
		PERCENT_MAPPED=$(awk "BEGIN { pc=(100*${ALIGNED}/${INITIAL}); print pc }");else
		PERCENT_MAPPED=0
	fi
	OUTPUT+="${PERCENT_MAPPED},"
	[ -f $sample/amended_consensus/*pad.fa ] && COV_BASES=$(tail -1 ${sample}/amended_consensus/*pad.fa | sed -s 's/N//g' | wc -c) || COV_BASES=0
	if [[ "spike" == $SPIKE ]]; then
		PERCENT_ASSEMBLED=$(awk "BEGIN { pc=(100*${COV_BASES}/3821); print pc }") && OUTPUT+="${PERCENT_ASSEMBLED},${COV_BASES},3821,";else
		PERCENT_ASSEMBLED=$(awk "BEGIN { pc=(100*${COV_BASES}/29905); print pc }") && OUTPUT+="${PERCENT_ASSEMBLED},${COV_BASES},29905,"
	fi
	[ -f $sample/tables/SARS-CoV-2-coverage.txt ] && DEPTH=$(awk '{ total += $3; count++ } END { print total/count }' ${sample}/tables/*-coverage.txt) || DEPTH=0
	OUTPUT+="${DEPTH}"


	OUTPUT+='\n'
done

echo -e $OUTPUT > $OUTFI
