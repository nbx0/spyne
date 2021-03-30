import zipfile
import io
import pandas as pd
from Bio import SeqIO
import dateutil.parser as dparser
from datetime import datetime
import re
from impala.dbapi import connect
import sqlalchemy
import impala.sqlalchemy
import pymysql
from os import rename, remove
from os.path import isdir, dirname, realpath, isfile, basename, expanduser
from subprocess import run
from hashlib import sha1
from time import sleep
import paramiko
from sys import argv
import tempfile
from getpass import getuser
hput=realpath(dirname(__file__))+'/ingest_scripts/hput'
if 'zag' in ' '.join(argv).lower():
	host='zag'
else:
	host='aspen'
ribosomeQsub = realpath(dirname(__file__))+'/ribosome_sge.sh'
dlpath = '/scicomp/groups/Projects/SARS2Seq/Resources/publicDBs/'

#reasonable assumption unless this is the clarity account
sshUser = getuser()
sshKeyFile = expanduser('~' + sshUser) + '/.ssh/id_rsa'
sshHost = 'aspen.biotech.cdc.gov'

hadoopHost = 'flu-hadoop-05.biotech.cdc.gov'
hadoopPort = 21050
hadoopDB = 'sars_cov2'
#CP changed the ncbi join to an anti-join. Contracotr nt_id has to be generated here for  now...please fix upstream
selectStatement = '''SELECT I.nt_id, 'SARS-CoV-2', sequence FROM gisaid_ingest as I LEFT ANTI JOIN genomes as G USING (nt_id) WHERE length(sequence) > 1000 
				UNION DISTINCT
				SELECT I.nt_id, 'SARS-CoV-2', sequence FROM ncbi_ingest as I LEFT ANTI JOIN genomes as G USING (nt_id) WHERE length(sequence) > 1000 	
				UNION DISTINCT
				SELECT I.nt_id, 'SARS-CoV-2', sequence FROM cdc_ingest_legacy as I LEFT ANTI JOIN genomes as G USING (nt_id) WHERE length(sequence) > 1000 
				UNION DISTINCT
				SELECT I.nt_id, 'SARS-CoV-2', sequence FROM cdc_production as I LEFT ANTI JOIN genomes as G USING (nt_id) WHERE length(sequence) > 1000 
				UNION DISTINCT
                                SELECT udx.nt_id(contractor_sequence) as nt_id, 'SARS-CoV-2', contractor_sequence as sequence FROM contractor_sequences  as I 
					LEFT ANTI JOIN genomes as G on udx.nt_id(contractor_sequence)  = G.nt_id WHERE length(contractor_sequence) > 1000
'''

def log(string, logfile=None):
	msg = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]\t{}".format(string))
	if logfile:
		with open(logfile, 'a+') as out:
			print(msg, logfile=out)
	else:
		print(msg)

def hadoop_to_dais_input():
	log('Gathering genomes from hadoop into dataframe')
	conn = connect(host=hadoopHost, port=hadoopPort, database=hadoopDB)
	df = pd.read_sql(selectStatement, conn)
	log('Dataframe loaded')
	log('Dataframe to sequences.tab started')
	tf = tempfile.NamedTemporaryFile(prefix=dlpath, delete=False)
	df.to_csv(tf.name, index=False, header=False, sep='\t')
	log('Dais input created: {}'.format(tf.name))
	return(tf.name)

def runRibosome(daisInputFile, host):
	if isfile('/opt/sge/bin/lx-amd64/qsub'):
		run(['/opt/sge/bin/lx-amd64/qsub', ribosomeQsub, daisInputFile, host ])
	else:
		ssh = paramiko.SSHClient()
		k = paramiko.RSAKey.from_private_key_file(sshKeyFile)
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=sshHost, username=sshUser, pkey=k)
		log('Launching DAIS-ribosome on Aspen over ssh')
		cmd = 'qsub {} {}'.format(ribosomeQsub, daisInputFile, host)
		ssh.exec_command(cmd)
def wait4ribosome(daisInputFile):
	print('Looking for {}.fin'.format(daisInputFile))
	while not isfile(daisInputFile+'.fin'):
		sleep(2)
	remove(daisInputFile+'.fin')

def loadHadoop(daisInputFile):
	log('Waiting for Ribosome to finish on Aspen (or locally) and return results')
	wait4ribosome(daisInputFile)
	log('Ribosome results returned from Aspen')
	log('Loading ribosome Hadoop tables')
	conn = connect(host=hadoopHost, port=hadoopPort, database=hadoopDB)
	dbc = conn.cursor()
	cmd = '{} {}.seq /user/nbx0/sars_cov2/alignments/'.format(hput, daisInputFile)
	run(cmd.split())
	cmd = '{} {}.ins /user/nbx0/sars_cov2/alignment_insertions/'.format(hput, daisInputFile)
	run(cmd.split())
	cmd = '{} {}.del /user/nbx0/sars_cov2/alignment_deletions/'.format(hput, daisInputFile)
	run(cmd.split())
	cmd = '{} {}.gen /user/nbx0/sars_cov2/genomes/'.format(hput, daisInputFile)
	run(cmd.split())
	cmd = '{} {}.gen.ins /user/nbx0/sars_cov2/genome_insertions/'.format(hput, daisInputFile)
	run(cmd.split())
	cmd = '{} {}.gen.del /user/nbx0/sars_cov2/genome_deletions/'.format(hput, daisInputFile)
	run(cmd.split())
	for i in ['alignments', 'alignment_insertions', 'alignment_deletions', 'genomes', 'genome_insertions', 'genome_deletions']:
		dbc.execute('refresh {}'.format(i))
	log('Finished loading Hadoop')

if __name__ == '__main__':
	fileName = hadoop_to_dais_input()
	runRibosome(fileName, host)
	loadHadoop(fileName)



