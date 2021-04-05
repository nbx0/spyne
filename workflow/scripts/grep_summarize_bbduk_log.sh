#!/usr/bin/env bash


# Input handling; confirm read access
infile="$(readlink -e "${1}")"

# Extract input total read and total nucleotide count
cnt_input_reads=$(grep '^Input: ' "${infile}" \
   | awk '{print $2}')
cnt_input_bases=$(grep '^Input: ' "${infile}" \
   | awk '{print $4}')

# Extract removed read and nucleotide counts
cnt_rm_reads=$(grep '^KTrimmed: ' "${infile}" \
   | awk '{print $2}' | sed 's/,//g')
cnt_rm_bases=$(grep '^KTrimmed: ' "${infile}" \
   | awk '{print $5}' | sed 's/,//g')

# Calculate output reads and nucleotides
cnt_output_reads="$(( ${cnt_input_reads} - ${cnt_rm_reads} ))"
cnt_output_bases="$(( ${cnt_input_bases} - ${cnt_rm_bases} ))"

# Form TSV information parsed from bbduk's logfile and send to stdout
nfo="${tot_reads} input reads\t${tot_bases} input basepairs\t"
nfo+="${rm_reads} removed reads\t${rm_bases} removed basepairs"
nfo+="${cnt_output_reads} output reads\t${cnt_output_bases} output basepairs"
echo -e "${nfo}"
