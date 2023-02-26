#!/usr/bin/env bash

# tar gzip archive spyne and IRMA logs
tar --remove-files -czf spyne_logs.tar.gz .snakemake logs IRMA/*/logs 

# tar gzip archive plurality fasta, F1*bam/ref
tar --remove-files -czf irma_allconsensus_bam.tar.gz IRMA/*/*fasta IRMA/*/intermediate/4-*/F1* IRMA/*/amended_consensus

# remove the rest of IRMAs output
rm -fr IRMA
