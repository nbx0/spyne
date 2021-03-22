import yaml
from glob import glob

with open('config.yaml', 'r') as y:
	config = yaml.safe_load(y)

for barcode in config['barcodes'].keys():
	fastqs = glob('guppy*/*/{}/*fastq.gz'.format(barcode))
	config['barcodes'][barcode]['fastqs'] = fastqs

with open('config.yaml', 'w') as out:
	yaml.dump(config, out, default_flow_style=False)
