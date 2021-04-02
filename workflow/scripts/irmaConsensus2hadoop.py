from glob import glob
from os.path import dirname, realpath, basename, getsize
from os import remove
from hashlib import sha1
from tempfile import NamedTemporaryFile
from impala.dbapi import connect
from subprocess import run
from sys import path, argv
from re import findall
import yaml
from datetime import datetime

with open('tests/config.yaml', 'r') as y: #hard coded for testing
	config = yaml.safe_load(y)

try:
	host=argv[1]
	tfname=''
	machine=config['machine']
	runid=config['runid']
except IndexError:
	host=False

path.append(dirname(dirname(realpath(__file__))))
from DAIS_from_hadoop import log, runRibosome, wait4ribosome, loadHadoop
import paramiko
runall=False
dlpath='/scicomp/scratch/nbx0/'

sshKeyFile = '/scicomp/home/nbx0/.ssh/id_rsa'

hadoopHost = 'flu-hadoop-05.biotech.cdc.gov'
hadoopPort = 21050
hadoopDB = 'sars_cov2'

hput = dirname(dirname(realpath(__file__)))+'/scripts/hput'

fastas = [i for i in glob('IRMA/*/amended_consensus/*pad.fa') if (not findall('[-_]V[0-9]',i) and getsize(i) >= 100) ]

ribosome = '/'.join(realpath(__file__).split('/')[:-3])+'/dais-ribosome/ribosome'

def findsampleid(filename, config):
	for k in config['barcodes'].keys():
		if k in filename:
			return k

tmpFile = open('hadoop/'+config['runid']+'_consensus.txt', 'w') # NamedTemporaryFile(prefix='', delete=False, mode='a+')
tmpFileDais = open('hadoop/'+config['runid'], 'w')  #NamedTemporaryFile(prefix=dlpath, delete=False, mode='a+')
for f in fastas:
	sampleid = findsampleid(f, config)
	with open(f, 'r') as d:
		d.readline()
		sequence = d.readline().upper().strip()
		sha =  sha1(sequence.encode()).hexdigest()
		tmpFile.write('\t'.join([config['machine'], config['runid'], config['barcodes'][sampleid]['csid'], config['barcodes'][sampleid]['cuid'], sequence, sha, config['barcodes'][sampleid]['clarityid'], config['barcodes'][sampleid]['Artifactid'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')])+'\n')
		tmpFileDais.write('\t'.join([sha, 'SARS-CoV-2', sequence])+'\n')
tmpFileDais.close()
tmpFile.close()

run([hput, tmpFile.name, '/user/nbx0/sars_cov2/cdc_production_all/'])

#conn = connect(host=hadoopHost, port=hadoopPort, database=hadoopDB)
#dbc = conn.cursor()
#dbc.execute('refresh cdc_production_all')
#runRibosome(realpath(tmpFileDais.name), host)
#print('Sending {} to loadHadoop function'.format(tmpFileDais.name))
#loadHadoop(tmpFileDais.name)
#for i in ['alignments', 'alignment_insertions', 'alignment_deletions', 'genomes', 'genome_insertions', 'genome_deletions']:
#	dbc.execute('refresh {}'.format(i))

