import pandas as pd
from argparse import ArgumentParser as AP
from sys import exit
import yaml
from impala.dbapi import connect
from subprocess import run
from os.path import dirname, realpath

hadoopHost = 'flu-hadoop-05.biotech.cdc.gov'
hadoopPort = 21050
hadoopDB = 'sars_cov2'
hput = dirname(dirname(realpath(__file__)))+'/ingest_scripts/hput'

p = AP(description='''Given files containing <sampleID> in filename from the SC2 pipeline, collects basic IRMA read count data and loads hadoop''')
r = p.add_argument_group('Required arguments')
r.add_argument('-s', '--samples',  metavar='<sampleID.file ... ...>', nargs='+')

try:
	args = p.parse_args()
except AttributeError:
	p.print_help()
	exit()

with open('config.yaml', 'r') as y:
	config = yaml.safe_load(y)

df = pd.DataFrame(columns=('machineid', 'runid', 'csid', 'cuid', 'totalreads', 
				'readspassedqc', 'readsmatchingref', 'clarityid', 'artifactid'))

def findsampleid(filename, config):
	for k in config['samples'].keys():
		if k in filename:
			return k

for filename in args.samples:
	sampleid = findsampleid(filename, config)
	totalreads, readspassedqc, readsmatchingref = 0, 0, 0
	try:
		with open('IRMA/{}/tables/READ_COUNTS.txt'.format(sampleid), 'r') as d:
			for line in d:
				if '1-initial' in line:
					totalreads = line.strip().split()[1]
				elif '2-passQC' in line:
					readspassedqc = line.strip().split()[1]
				elif '3-match' in line:
					readsmatchingref = line.strip().split()[1]
	except FileNotFoundError:
		pass
	df = df.append({'machineid':config['machine'],
				'runid':config['runid'],
				'csid':config['samples'][sampleid]['csid'],
				'cuid':config['samples'][sampleid]['cuid'],
				'totalreads':totalreads,
				'readspassedqc':readspassedqc,
				'readsmatchingref':readsmatchingref,
				'clarityid':config['samples'][sampleid]['clarityid'],
				'artifactid':config['samples'][sampleid]['Artifactid']}, ignore_index=True)
df.to_csv('hadoop/basicIrmaReadCounts.txt', sep='\t', index=False, header=False, mode='w')
#run([hput, 'hadoop/basicIrmaReadCounts.txt', '/user/nbx0/sars_cov2/irmareadcounts/{}_{}.txt'.format(config['machine'], config['runid'])])		
conn = connect(host=hadoopHost, port=hadoopPort, database=hadoopDB)
dbc = conn.cursor()
dbc.execute('refresh irmareadcounts')

