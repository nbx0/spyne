# On-Premises ONT Assembly

Snakemake workflow specifically for ONT data processing with CDC-specific infrastructure


## General Steps of the Pipeline
1. remove barcodes from FastQ reads that were not removed due to having a few SNPs with `bbduk.sh`
2. trim primers from ends with `cutadapt`
3. perform genome assembly with `irma` to generate a FastA consensus sequence






#### Dependencies
The workflow scripts require:
- Python
- Snakemake
System calls make use of:
- bbtools
- cutadapt
- IRMA


#### Resources
- snakemake has an official tutorial section [here](https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html#tutorial)
- [10 recommendations for software by Torsten](https://gigascience.biomedcentral.com/articles/10.1186/2047-217X-2-15)
