#!/usr/bin/env bash


# Input handling; confirm read access
infile="$(readlink -e "${1}")"

# Extract input total read and total nucleotide count
cnt_input_reads=$(grep '^Total reads' "${infile}" \
   | awk '{print $4}' | sed 's/,//g')
cnt_input_bases=$(grep '^Total basepairs' "${infile}" \
   | awk '{print $4}' | sed 's/,//g')

# Extract reads and nucleotides output
cnt_output_reads=$(grep '^Reads written (passing filters):' "${infile}" \
   | awk '{print $5}' | sed 's/,//g')
cnt_output_bases=$(grep '^Total written (filtered):' "${infile}" \
   | awk '{print $4}' | sed 's/,//g')

# Calculate read and nucleotide removal counts
cnt_rm_reads="$(( ${cnt_input_reads} - ${cnt_output_reads} ))"
cnt_rm_bases="$(( ${cnt_input_bases} - ${cnt_output_bases} ))"

# Form TSV information parsed from cutadapt's logfile and send to stdout
nfo="${cnt_input_reads} input reads\t${cnt_input_bases} input bases\t"
nfo+="${cnt_rm_reads} removed reads\t${cnt_rm_bases} removed basepairs"
nfo+="${cnt_output_reads} output reads \t${cnt_output_bases} output bases"
echo -e "${nfo}"
