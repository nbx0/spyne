#!/usr/bin/env bash


# I/O handling
irmaconfig=$1
read1=$2
samplename=$3
if [[ -z $(which IRMA) ]]; then
  echo "ERROR: add IRMA to path" && exit 0
fi

# Executing this script removes any precomputed temporary data
if [[ -d "IRMA/_${samplename}" ]]; then
  rm -fr "IRMA/_${samplename}"
fi

spath=/scicomp/home-pure/sars2seq/prod


# With an empty perllib, run IRMA with a temp hidden outdir, and only if
#  successful make the temp outdir visible to users
PERL5LIB='' && \
 ${spath}/irma/IRMA "${irmaconfig}" "${read1}" "IRMA/_${samplename}" && \
 mv "IRMA/_${samplename}" "IRMA/${samplename}" && sleep 20
