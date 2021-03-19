#!/bin/bash

#$ -q all.q
#$ -cwd
#$ -V
#$ -b y
#$ -N mia2

root=$(dirname $0)
args="--cluster \"qsub \
					-q short.q,all.q,highmem.q \
					-cwd \
					-V \
					-b y \
					-pe smp {threads} \
					-o logs/cluster/mia2.{name}.{jobid}.out \
					-e logs/cluster/mia2.{name}.{jobid}.err\" \
		--cores 1000 \
		--jobname \"mia2.{name}.{jobid}.sh\" "

cmd="snakemake -s ${root}/Snakefile --cores 64 --printshellcmds --configfile config.yaml ${args}"
echo $cmd
eval $cmd && success=$?
