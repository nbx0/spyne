#!/bin/bash

irmaconfig=$1
read1=$2
samplename=$3

[[ -d IRMA/_${samplename} ]] && rm -fr IRMA/_${samplename}
spath=$(dirname $0)
irma=$(cd $spath && readlink -f ../../../irma/IRMA)
PATH=$(dirname $irma):${PATH}
PERL5LIB="" &&\
$irma $irmaconfig $read1 IRMA/_${samplename} && mv IRMA/_${samplename} IRMA/${samplename} #&& sleep 20
