#!/usr/bin/env bash

fastqs=$@
sample_name=$(echo $fastqs|cut -f1 |rev|cut -d '/' -f1|rev | cut -d '.' -f1)
sample_name=${sample_name#cat_}
docker run --rm \
  -v $PWD:/data \
  public.ecr.aws/n3z8t4o2/irma:1.0.2p3 \
  IRMA FLU-minion $fastqs $sample_name

[[ ! -d IRMA ]] && mkdir IRMA
mv $sample_name IRMA/