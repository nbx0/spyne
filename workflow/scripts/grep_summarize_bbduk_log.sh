#!/usr/bin/env bash


tot_reads=$(grep '^Input: ' $1 \
   | awk '{print $2}')
tot_bases=$(grep '^Input: ' $1 \
   | awk '{print $4}')

rm_reads=$(grep '^KTrimmed: ' $1 \
   | awk '{print $2}' | sed 's/,//g')
rm_bases=$(grep '^KTrimmed: ' $1 \
   | awk '{print $5}' | sed 's/,//g')

nfo="${tot_reads} input reads\t${tot_bases} input basepairs\t"
nfo+="${rm_reads} removed reads\t${rm_bases} removed basepairs"
echo -e "${nfo}"
