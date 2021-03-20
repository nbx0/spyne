# On-Premises ONT Assembly

Snakemake workflow specifically for ONT data processing with CDC-specific infrastructure


## General Steps of the Pipeline
1. remove barcodes from FastQ reads that were not removed due to having a few SNPs with `bbduk.sh`
2. discard low quality reads with `cutadapt`
3. perform genome assembly with `irma` to generate a FastA consensus sequence
4. align ... ???
5. re-align ... ???
6. ???

### Install environment to run the snakemake workflow
1. Install conda or miniconda so that you have `conda` available
```
wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh --directory-prefix "${HOME}/Downloads"
bash "${HOME}/Downloads/Anaconda3-2020.11-Linux-x86_64.sh
# install to ~/.anaconda3 is better than the visibly distracting ~/anaconda3 default
echo 'export PATH="${HOME}/.anaconda3/bin:${PATH}"' >> "${HOME}/.bashrc"
source ~/.bashrc
```

2. Create a new conda environment called "snake-env". The file lists libraries (e.g., pandas) and packages (e.g., minimap2) along with specific versions to install. Note by specifying the prefix, the environment name is also set.
```
conda env create --file environment.yml --prefix /scicomp/home-pure/sars2seq/.miniconda3_biolinux/env/snake-env
conda activate snake-env
# shorten that long PS1 with a one-time config change
conda config --set env_prompt '($(basename {name})) '
conda deactivate
# from now on, going into environments will only show its basename
# we can also make make activating the environment quicker
echo "alias activate_snake='source activate /scicomp/home-pure/sars2seq/.miniconda3_biolinux/env/snake-env'" >> "${HOME}/.bashrc"
source ~/.bashrc
activate_snake
```

3. Manually download and place IRMA within the conda environment (??cant test IRMA yet??)
```
wget https://wonder.cdc.gov/amd/flu/irma/flu-amd-202103.zip --directory-prefix /scicomp/home-pure/sars2seq/.miniconda3_biolinux/env/snake-env/bin
unzip /scicomp/home-pure/sars2seq/.miniconda3_biolinux/env/snake-env/bin/flu-amd-202103.zip -d /scicomp/home-pure/sars2seq/.miniconda3_biolinux/env/snake-env/bin
rsync -avh /scicomp/home-pure/sars2seq/.miniconda3_biolinux/env/snake-env/bin/flu-amd/ /scicomp/home-pure/sars2seq/.miniconda3_biolinux/env/snake-env/bin
rm -r /scicomp/home-pure/sars2seq/.miniconda3_biolinux/env/snake-env/bin/flu-amd
```


#### Dependencies
- Python
- Snakemake
- bbtools
- cutadapt
- IRMA


#### Resources
- snakemake has an official tutorial section [here](https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html#tutorial)
