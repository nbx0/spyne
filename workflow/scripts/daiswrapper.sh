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
[[ ! -d IRMA/dais_results ]] && mkdir IRMA/dais_results
cmd="docker run --rm \
    -v $PWD:/data \
    public.ecr.aws/n3z8t4o2/dais-ribosome:1.2.1 ribosome \
    --module $MODULE $input ${dais_out}.seq ${dais_out}.ins ${dais_out}.del"

echo $cmd
eval $cmd

mv ${dais_out}* IRMA/dais_results
