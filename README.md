# On-Premises ONT Assembly

Snakemake workflow specifically for ONT data processing with CDC-specific infrastructure


## General Steps of the Pipeline
1. remove barcodes from FastQ reads that were not removed due to having a few SNPs with `bbduk.sh`
2. trim primers from ends with `cutadapt`
3. perform genome assembly with `irma` to generate a FastA consensus sequence
4. confirm successful assembly and prepare for Hadoop upload


## Working Environment
These steps must be done to use the workflow and to use snakemake, snake, and slither environments:
```
if [ -z "${SARS2_ONT_HOME}" ]; then
  echo "SARS2_ONT_HOME='/scicomp/home-pure/sars2seq/.on-premises-ont-assembly-development/'" >> "${HOME}/.bashrc"
else
  echo -e '\nyou already have the `SARS2_ONT_HOME` environment variable set in your bashrc'
fi
if ! grep -q 'activate_snakemake' ~/.bashrc; then
  echo $'alias activate_snakemake=\'export PATH=${SARS2_ONT_HOME}.anaconda3/bin:${PATH} && source activate ${SARS2_ONT_HOME}.anaconda3/env/snakemake\'' >> "${HOME}/.bashrc"
else
  echo -e '\nyou already have the `activate_snakemake` alias in your bashrc'
fi
if ! grep -q 'activate_snake' ~/.bashrc; then
  echo $'alias activate_snake=\'export PATH=${SARS2_ONT_HOME}.anaconda3/bin:${PATH} && source activate ${SARS2_ONT_HOME}.anaconda3/env/snake\'' >> "${HOME}/.bashrc"
else
  echo -e '\nyou already have the `activate_snake` alias in your bashrc'
fi
if ! grep -q 'activate_slither' ~/.bashrc; then
  echo $'alias activate_slither=\'export PATH=${SARS2_ONT_HOME}.anaconda3/bin:${PATH} && source activate ${SARS2_ONT_HOME}.anaconda3/env/slither\'' >> "${HOME}/.bashrc"
else
  echo -e '\nyou already have the `activate_slither` alias in your bashrc'
fi
```
To avoid collisions with other development projects, we have our own separate path where this and all of its dependencies are available. `/scicomp/home-pure/sars2seq/.on-premises-ont-assembly-development/` is the main path to be set with the environment variable `$SARS2_ONT_HOME` in your ~/.bashrc This will enable us to replace this later easily for packaging. We have conda environments "snakemake", "snake", and "slither" that won't disrupt any of your other conda installs or environments if you use the alias "activate_snakemake", "activate_snake", or "activate_slither".


### How our environments were installed to run the snakemake workflow
1. Install conda but don't have it disrupt any of your other conda installs or environments
```
wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh --directory-prefix "${HOME}/Downloads"
bash "${HOME}/Downloads/Anaconda3-2020.11-Linux-x86_64.sh"
# install to "${SARS2_ONT_HOME}.anaconda3" is better than the visibly distracting ~/anaconda3 default
export PATH="${SARS2_ONT_HOME}.anaconda3/bin:${PATH}"
```
2.a. Create a new conda environment called "snakemake". The file lists libraries (e.g., pandas) and packages (e.g., minimap2) along with specific versions to install. Note by specifying the prefix, the environment name is also set.
```
conda install --yes mamba
git clone git@git.biotech.cdc.gov:ylo1/on-premises-ont-assembly.git "${SARS2_ONT_HOME}"on-premises-ont-assembly
mamba env create --file "${SARS2_ONT_HOME}on-premises-ont-assembly/env/snakemake_environment.yml" --prefix "${SARS2_ONT_HOME}".anaconda3/env/snakemake
source activate "${SARS2_ONT_HOME}.anaconda3/env/snakemake"
# shorten that long PS1 with a one-time config change
conda config --set env_prompt '($(basename {name})) '
conda deactivate
# from now on, going into environments will only show its basename
# we can also make make activating the environment quicker
echo $'alias activate_snakemake=\'export PATH=${SARS2_ONT_HOME}.anaconda3/bin:${PATH} && source activate ${SARS2_ONT_HOME}.anaconda3/env/snakemake\'' >> "${HOME}/.bashrc"
source ~/.bashrc
activate_snakemake
```

2.b. Create a new conda environment called "snake".
```
mamba env create --file "${SARS2_ONT_HOME}on-premises-ont-assembly/env/snake_environment.yml" --prefix "${SARS2_ONT_HOME}".anaconda3/env/snake
```

2.c. Create a new conda environment called "slither".
```
mamba env create --file "${SARS2_ONT_HOME}on-premises-ont-assembly/env/slither_environment.yml" --prefix "${SARS2_ONT_HOME}".anaconda3/env/slither
```

3. Manually download and place IRMA only within the "slither" conda environment
```
wget https://wonder.cdc.gov/amd/flu/irma/flu-amd-202103.zip --directory-prefix "${SARS2_ONT_HOME}".anaconda3/env/slither/bin
unzip "${SARS2_ONT_HOME}.anaconda3/env/slither/bin/flu-amd-202103.zip" -d "${SARS2_ONT_HOME}.anaconda3/env/slither/bin"
rsync -avh "${SARS2_ONT_HOME}.anaconda3/env/slither/bin/flu-amd/" "${SARS2_ONT_HOME}.anaconda3/env/slither/bin"
rm -r "${SARS2_ONT_HOME}.anaconda3/env/slither/bin/flu-amd"
IRMA --help
```
<!-- # remove tools that should be packaged
rm -v ${SARS2_ONT_HOME}.anaconda3/env/slither/bin/IRMA_RES/scripts/*{blat,minimap2,parallel,pigz,samtools}*
rm -v ${SARS2_ONT_HOME}.anaconda3/env/slither/bin/LABEL_RES/scripts/*{FastTreeMP,muscle,parallel,shogun}*
# align2model,hmmscore,modelfromalign all within sam3.5 need'to find online
mamba install blat minimap2 parallel pigz samtools fasttree muscle shogun -y
$ -->

### Run a Test Example (within this repository)
```
# simplest example
cd on-premises-ont-assembly
activate_slither
snakemake -s workflow/Snakefile --cores 6 --printshellcmds
# optionally use individual conda environments for each step
snakemake -s workflow/Snakefile --cores 6 --printshellcmds --use-conda --conda-frontend mamba
```


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
