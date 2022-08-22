# On-Premises ONT Assembly for Spike Only Sequencing
a
Snakemake workflow specifically for ONT data processing with any infrastructure


## General Steps of the Pipeline
1. remove barcodes from FastQ reads that were not removed due to having a few SNPs with `bbduk.sh`
2. trim primers from ends with `cutadapt`
3. perform genome assembly with `irma` to generate a FastA consensus sequence



## To run Pipeline
1. Export IRMA, bbtools (bbduk.sh, reformat.sh) to path
2. Activate conda environment
ex: 
` source /scicomp/groups/Projects/SARS2Seq/bin/miniconda/bin/activate /scicomp/home-pure/sars2seq/miniconda/envs/snakemake`
3. Create samplesheet.csv
4. Create config.yaml from samplesheet

` python scripts/config_create.py <path to samplesheet.csv> <path to instrument run> <Nanopore run name> `

5. Run Snakemake


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
