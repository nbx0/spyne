import yaml
from os.path import abspath
from sys import argv, exit

root = '/'.join(abspath(__file__).split('/')[:-3])

if len(argv) != 4:
	exit('\n\tUSAGE: {} <samplesheet.csv> <flowcell> <machine>\n'.format(__file__))

data = {'machine':argv[3], 'flowcell':argv[2], 'irmamodule':'CoV-minion-long-reads', 'barcodes':{}}

with open('{}/resources/ont_barcodes.yaml'.format(root), 'r') as y:
	barseqs = yaml.safe_load(y)

def reverse_complement(seq):
    rev = {'A':'T','T':'A','C':'G','G':'C'}
    seq = seq[::-1]
    return ''.join(rev[i] for i in seq)

with open(argv[1], 'r') as d:
	for line in d:
		l = line.split()
		data['barcodes'][l[0]] = {'sample':l[1], 'barcode_sequence':barseqs[l[0]], 'barcode_sequence_rc':reverse_complement(barseqs[l[0]])}

with open('config.yaml', 'w') as out:
	yaml.dump(data, out, default_flow_style=False)


