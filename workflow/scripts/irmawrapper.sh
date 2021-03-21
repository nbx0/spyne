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

# Activate "slither" conda env which contains IRMA and its dependencies
export PATH="${SARS2_ONT_HOME}.anaconda3/bin:${PATH}"
source activate "${SARS2_ONT_HOME}.anaconda3/env/slither"

# With an empty perllib, run IRMA with a temp hidden outdir, and only if
#  successful make the temp outdir visible to users
PERL5LIB='' && \
 IRMA "${irmaconfig}" "${read1}" "IRMA/.${samplename}" && \
 mv "IRMA/.${samplename}" "IRMA/${samplename}"
