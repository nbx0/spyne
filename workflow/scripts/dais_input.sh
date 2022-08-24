#!/usr/bin/env bash
declare -A IAV
IAV['PB2']=1
IAV['PB1']=2
IAV['PA']=3
IAV['HA']=4
IAV['NP']=5
IAV['NA']=6
IAV['M']=7
IAV['MP']=7
IAV['NS']=8
IAV[1]='PB2'
IAV[2]='PB1'
IAV[3]='PA'
IAV[4]='HA'
IAV[5]='NP'
IAV[6]='NA'
IAV[7]='M'
IAV[8]='NS'
[[ -f {input} ]] || \
for ((i=1;i<9;i++)); do 
    cat IRMA/*/amended_consensus/*${i}*.fa >> IRMA/all_${IAV[$i]}.fasta
done && \
cat IRMA/*/amended_consensus/*fa <(curl https://raw.githubusercontent.com/nbx0/NGS_training/master/lib/DAIS-Ribosome_refs/A_H1_H3_refs.fasta) 