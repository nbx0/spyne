import yaml
from os.path import abspath
from sys import argv, exit
import pandas as pd
from glob import glob
import subprocess
import os


root = "/".join(abspath(__file__).split("/")[:-2])
if len(argv) < 2:
    exit(
        "\n\tUSAGE: {} <samplesheet.csv> <runpath> <experiment_type>\n".format(__file__)
    )

try:
    runpath = argv[2]
    experiment_type = argv[3]
except (IndexError, ValueError):
    runid = "testRunID"
df = pd.read_csv(argv[1])
dfd = df.to_dict("index")

if 'ont' in experiment_type.lower():
    if 'fastq_pass' in runpath:
        data = {'runid':runpath.split('/')[runpath.split('/').index('fastq_pass') -1], 'barcodes':{}}
    else:
        data = {'runid':runpath.split('/')[-1], 'barcodes':{}}
    def reverse_complement(seq):
        rev = {"A": "T", "T": "A", "C": "G", "G": "C", ",": ","}
        seq = seq[::-1]
        return "".join(rev[i] for i in seq)

    failures = ""
    try:
        with open(
            "{}/lib/EXP-NBD196.yaml".format(root), "r"
        ) as y:
            barseqs = yaml.safe_load(y)
    except:
        with open(
            "{}/lib/EXP-NBD196.yaml".format(root), "r"
        ) as y:
            barseqs = yaml.safe_load(y)
    for d in dfd.values():
        if 'fastq_pass' in runpath:
            fastq_pass = glob(runpath + '/*/')
        else:
            fastq_pass = glob(runpath + '/fastq_pass/*/')
        if d['Barcode #'] in [x.split("/")[-2] for x in fastq_pass]:

            data["barcodes"][d["Sample ID"]] = {
                "sample_type": d["Sample Type"],
                "barcode_number": d["Barcode #"],
                "barcode_sequence": barseqs[d["Barcode #"]],
                "barcode_sequence_rc": reverse_complement(barseqs[d["Barcode #"]]),
            }
        else:
            failures += str(d["Barcode #"]) + "\n"

    if len(failures) > 1:
        print("failed samples detected: Barcodes\n", failures.strip())
else:
    data = {'runid':runpath.split('/')[-1], 'samples':{}}
    for d in dfd.values():
        id = d['Sample ID']
        R1_fastq = glob(f"{runpath}/**/{id}*R1*fastq.gz")[0]
        print(R1_fastq)
        R2_fastq = glob(f"{runpath}/**/{id}*R2*fastq.gz")[0]
        if len(R1_fastq) < 1 or len(R2_fastq) < 1:
            print(f"Fastq pair not found for sample {id}")
            exit()
        data["samples"][d["Sample ID"]] = {
                "sample_type": d["Sample Type"],
                "R1_fastq": R1_fastq.replace(f'{runpath}/',''), 
                "R2_fastq": R2_fastq.replace(f'{runpath}/',''), 
            }
with open(runpath.replace("fastq_pass", "") + "/config.yaml", "w") as out:
    yaml.dump(data, out, default_flow_style=False)

snakefile_path = f"{root}/workflow/"
if "ont" in experiment_type.lower():

    if "flu" in experiment_type.lower():
        snakefile_path += "influenza_snakefile"
    elif "sc2" in experiment_type.lower():
        snakefile_path += "sc2_spike_snakefile"
else:
    snakefile_path += "illumina_influenza_snakefile"

if "TESTDEV-QUICK" in argv:
    snake_cmd = (
        f"snakemake -s {snakefile_path} \
        --configfile config.yaml \
        --cores 4 	\
        --printshellcmds \
        --rerun-incomplete"
    )
elif "TESTDEV-PRINTDAG" in argv:
    snake_cmd = (
        f"snakemake -s {snakefile_path} \
        --configfile config.yaml \
        --cores 4 	\
        --printshellcmds \
        --dag |awk '/digraph/,/\u007d/' |dot -Tpdf > filegraph.pdf"
    ) 
elif "TESTDEV-DEBUGDAG" in argv:
    snake_cmd = (
        f"snakemake -s {snakefile_path} \
        --configfile config.yaml \
        --cores 4 	\
        --printshellcmds \
        --debug-dag"
    ) 
else:
    snake_cmd = (
            f"snakemake -s {snakefile_path} \
            --configfile config.yaml \
            --cores 4 	\
            --printshellcmds \
    	    --restart-times 10 \
    	    --rerun-incomplete \
    	    --latency-wait 600 "
        )
os.chdir(runpath.replace("fastq_pass", ""))
print(f"\n\nSNAKEMAKE CMD:\n {snake_cmd}\n\n")
subprocess.run(snake_cmd, shell=True)

# Remove extraneous intermediate files and tar archive logs, F1 bam and plurality consensus
if "CLEANUP-FOOTPRINT" in argv:
    fullsize = int(subprocess.run(f"du -d0", stdout=subprocess.PIPE, shell=True).stdout.decode().split('\t')[0])
    subprocess.run(f"{root}/workflow/scripts/spyne_cleanup.sh", shell=True)
    cleansize = int(subprocess.run(f"du -0", stdout=subprocess.PIPE, shell=True).stdout.decode().split('\t')[0])
    removed = fullsize - cleansize
    print(f"{removed/1000:.2f}MB removed\n{cleansize/1000:.2f}MB remain")
