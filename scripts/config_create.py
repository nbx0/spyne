import yaml
from os.path import abspath
from sys import argv, exit
import pandas as pd
from glob import glob
import subprocess

root = "/".join(abspath(__file__).split("/")[:-2])

if len(argv) < 1:
    exit("\n\tUSAGE: {} <samplesheet.csv> <run_id> <kit>\n".format(__file__))

runid, kit = argv[2:4]

data = {"runid": runid, "barcodes": {}, "kit": kit}


def reverse_complement(seq):
    rev = {"A": "T", "T": "A", "C": "G", "G": "C", ",": ","}
    seq = seq[::-1]
    return "".join(rev[i] for i in seq)


df = pd.read_csv(argv[1])
dfd = df.to_dict("index")
failures = ""
try:
    with open(
        "{}/lib/{}.yaml".format(root, dfd[0]["Barcode_expansion_pack"]), "r"
    ) as y:
        barseqs = yaml.safe_load(y)
except:
    with open("{}/lib/{}.yaml".format(root, kit, "r")) as y:
        barseqs = yaml.safe_load(y)
for d in dfd.values():
    fastq_pass = glob(f"{d['barcode']}/*fastq*")
    if d["barcode"] in [x.split("/")[-2] for x in fastq_pass]:

        data["barcodes"][d["sample name"]] = {
            "kit": kit,
            "sample_id": d["sample name"],
            "barcode_number": d["barcode"],
            "barcode_sequence": barseqs[d["barcode"]],
            "barcode_sequence_rc": reverse_complement(barseqs[d["barcode"]]),
        }
    else:
        failures += d["barcode"] + "\n"
with open("config.yaml", "w") as out:
    yaml.dump(data, out, default_flow_style=False)

if len(failures) > 1:
    print("failed samples detected:\n", failures.strip())
