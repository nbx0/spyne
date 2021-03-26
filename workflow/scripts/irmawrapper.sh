#!/usr/bin/env bash


# I/O handling
irmaconfig=$1
read1=$2
samplename=$3
if [[ -z "${SARS2_ONT_HOME}" ]]; then
  SARS2_ONT_HOME='/scicomp/home-pure/sars2seq/.on-premises-ont-assembly-development/'
fi

# Executing this script removes any precomputed temporary data
if [[ -d "IRMA/.${samplename}" ]]; then
  rm -fr "IRMA/.${samplename}"
fi

spath=/scicomp/home-pure/sars2seq/prod


# With an empty perllib, run IRMA with a temp hidden outdir, and only if
#  successful make the temp outdir visible to users
PERL5LIB='' && \
 ${spath}/irma/IRMA "${irmaconfig}" "${read1}" "IRMA/.${samplename}" && \
 mv "IRMA/.${samplename}" "IRMA/${samplename}"
