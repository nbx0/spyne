#!/usr/bin/env bash


# Input handling; confirm read access
infile="$(readlink -e "${1}")"

# Extract input total read and total nucleotide count
cnt_input_reads=$(grep '^Total reads' "${infile}" \
   | awk '{print $4}' | sed 's/,//g')
cnt_input_bases=$(grep '^Total basepairs' "${infile}" \
   | awk '{print $4}' | sed 's/,//g')

# Extract adapter removal counts, calculate output read count,
#  and extract total nucleotide output
cnt_adapters=$(grep '^Reads with adapters:' "${infile}" \
   | awk '{print $4}' | sed 's/,//g')
cnt_output_reads=$(( "${cnt_input_reads}" - "${cnt_adapters}" ))
cnt_output_bases=$(grep '^Total written' "${infile}" \
   | awk '{print $4}' | sed 's/,//g')

# Form TSV information parsed from cutadapt's logfile and send to stdout
nfo="${cnt_input_reads} input reads\t${cnt_input_bases} input bases\t"
nfo+="${cnt_output_reads} output reads \t${cnt_output_bases} output bases"
echo -e "${nfo}"
