#!/usr/bin/env bash
while getopts 'i:m:' OPTION
do
	case $OPTION in
	i ) input=$OPTARG;; 
	m ) MODULE=$OPTARG;;
	esac
done

sed -i 's/-/_/g' $input || sed -i 's/-/_/g' $(basename $input)

dais_out=$(echo $input|cut -d '.' -f 1)
dais_out=${dais_out%"_input"} 

[[ ! -d IRMA/dais_results ]] && mkdir IRMA/dais_results
cmd="docker exec  \
    dais-ribosome-1.2.1 ribosome \
    --module $MODULE $input ${dais_out}.seq ${dais_out}.ins ${dais_out}.del"

echo $cmd
eval $cmd && \
sleep 10 && \
mv ${dais_out}* IRMA/dais_results || mv DAIS* IRMA/dais_results
