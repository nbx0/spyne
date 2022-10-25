#!/usr/bin/env bash
while getopts 'i:m:' OPTION
do
	case $OPTION in
	i ) input=$OPTARG;; 
	m ) MODULE=$OPTARG;;
	esac
done
echo $input
readlink -f $input
dais_out=$(echo $input|cut -d '.' -f 1) 
[[ ! -d DAIS ]] && mkdir DAIS
cmd="docker run --rm \
    -v $PWD:/data \
    public.ecr.aws/n3z8t4o2/dais-ribosome:1.2.1 ribosome \
    --module $MODULE $input ${dais_out}.seq ${dais_out}.ins ${dais_out}.del"

echo $cmd
eval $cmd

mv ${dais_out}* DAIS/
cd DAIS
for i in $(cut --output-delimiter=".+" -f 3,4 ${dais_out}.seq |sort |uniq |grep -v '\\N')
    do grep -E "${i}\s" ${dais_out}.seq | sed 's/^/>/' |cut -f 1,4,6| sed 's/\t/_/' |tr '\t' '\n' > $(echo $i |cut -d '+' -f 2)_ORF.fasta &&\
     wslview $(echo $i |cut -d '+' -f 2)_ORF.fasta
done