import yaml
from os.path import abspath
from sys import argv, exit
import pandas as pd
from glob import glob

root = '/'.join(abspath(__file__).split('/')[:-2])


############### IN TESTING
# FASTQ location is hardcoded here. Needs to be updated for production.
searchDir = '/'.join(abspath(argv[1]).split('/')[:-1])
fastqs=glob('{}/**/*.fastq.gz'.format(searchDir), recursive=True)
###################


if len(argv) < 1:
	exit('\n\tUSAGE: {} <samplesheet.csv> <machine> <runid>\n'.format(__file__))

try:
	machine,runid = argv[2:4]
except (IndexError, ValueError):
	machine,runid = 'testMachine','testRunID'

data = {'runid':runid, 'machine':machine, 'irmamodule':'CoV-minion-long-reads', 'barcodes':{}}

def reverse_complement(seq):
    rev = {'A':'T','T':'A','C':'G','G':'C'}
    seq = seq[::-1]
    return ''.join(rev[i] for i in seq)

df = pd.read_csv(argv[1])
dfd = df.to_dict('index')
#print(dfd)
with open('{}/lib/{}.yaml'.format(root, dfd[0]['kit']), 'r') as y:
	barseqs = yaml.safe_load(y)

for d in dfd.values():
	clarityid, csid, cuid, artifactid = d['alias'].split('_')
	data['barcodes'][d['barcode']] = {'clarityid':clarityid,
									'csid':csid,
									'cuid':cuid,
									'artifactid':artifactid,
									'Library':'swift',
									'flow_cell_id':d['flow_cell_id'],
									'flow_cell_product_code':d['flow_cell_product_code'],
									'kit':d['kit'],
									'sample_id':d['sample_id'],
									'experiment_id':d['experiment_id'],
									'barcode_sequence':barseqs[d['barcode']],
									'barcode_sequence_rc':reverse_complement(barseqs[d['barcode']]),
									'fastqs':fastqs}

with open('config.yaml', 'w') as out:
	yaml.dump(data, out, default_flow_style=False)


