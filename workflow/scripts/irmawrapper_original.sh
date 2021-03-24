#!/bin/bash

if [[ $# -eq 4 ]]; then
        irmaconfig=$1
        reads="$2 $3"
        samplename=$4
else
        irmaconfig=$1
        reads=$2
        samplename=$3
fi

spath=''
[[ -d IRMA/${samplename} ]] && touch IRMA/${samplename}.fin && exit 0
[[ -d IRMA/_${samplename} ]] && mv  IRMA/_${samplename} IRMA/${samplename} && touch IRMA/${samplename}.fin && exit 0
PATH=${spath}/label/:${PATH}
PERL5LIB="" &&\
${spath}/irma/IRMA $irmaconfig $reads IRMA/_${samplename} && mv IRMA/_${samplename} IRMA/${samplename} && sleep 20

