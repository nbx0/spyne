#!/usr/bin/env bash


# Input handling; confirm read access
infile="$(readlink -e "${1}")"

# Extract input total read and total nucleotide count
cnt_input_reads=$(grep '^Input:' "${infile}" \
   | awk '{print $2}')
cnt_input_bases=$(grep '^Input:' "${infile}" \
   | awk '{print $4}')

# Extract output read and nucleotide counts
cnt_output_reads=$(grep '^Output:' "${infile}" \
   | awk '{print $2}')
cnt_output_bases=$(grep '^Output:' "${infile}" \
   | awk '{print $5}')

# Calculate removed reads and nucleotides
cnt_discarded_reads="$(( ${cnt_input_reads} - ${cnt_output_reads} ))"
cnt_discarded_bases="$(( ${cnt_input_bases} - ${cnt_output_bases} ))"

# Form TSV information parsed from reformat's logfile and send to stdout
nfo="${cnt_input_reads} input reads\t${cnt_input_bases} input basepairs\t"
nfo+="${cnt_discarded_reads} removed reads\t${cnt_discarded_bases} removed basepairs"
nfo+="${cnt_output_reads} output reads\t${cnt_output_bases} output basepairs"
echo -e "${nfo}"
