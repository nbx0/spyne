from argparse import ArgumentParser as AP
from os.path import realpath, dirname
import yaml
from sys import exit
from subprocess import run
from glob import glob

p = AP(description='''Provide a config.yaml and /hadoop directory and script reloads all SC2 hadoop tables''')
r = p.add_argument_group('Required arguments')
r.add_argument('-c', '--config', nargs=1, required=True)
r.add_argument('-d', '--hadoop_dir', nargs=1, required=True)

try:
	args = p.parse_args()
except AttributeError:
	p.print_help()
	exit()

hput = dirname(realpath(__file__))+'/hput'
himpala = dirname(realpath(__file__))+'/himpala'

with open(args.config[0], 'r') as y:
	config = yaml.safe_load(y)

hadoopDir = args.hadoop_dir[0]

bbdukstats = glob(hadoopDir+'/*_bbdukstats.txt')[0]
irmaReadStats = hadoopDir+'/basicIrmaReadCounts.txt'
ampCov = hadoopDir+'/all_amplicon_coverage.txt'
irmaIns = hadoopDir+'/all_insertions_realign.txt'
irmaDel = hadoopDir+'/all_deletions_realign.txt'
irmaCov = hadoopDir+'/all_coverage_realign.txt'
irmaAll = hadoopDir+'/all_allAlleles_realign.txt'
irmaConsensus = glob(hadoopDir+'/*_consensus.txt')[0]
daisIns = [i for i in glob(hadoopDir+'/*.ins') if 'gen' not in i][0]
daisDel = [i for i in glob(hadoopDir+'/*.del') if 'gen' not in i][0]
daisSeq = glob(hadoopDir+'/*.seq')[0]
daisGen = glob(hadoopDir+'/*.gen')[0]
daisGenIns = glob(hadoopDir+'/*.gen.ins')[0]
daisGenDel = glob(hadoopDir+'/*.gen.del')[0]
benchmark = hadoopDir+'/benchmarks.txt'
config_parquet = glob(hadopDir+'/parquet/*parquet')

def loadHadoop(file, table, hadoopfilename):
	print('Loading {} to /user/nbx0/sars_cov2/{}/{}'.format(file, table, hadoopfilename))
	run([hput, file, '/user/nbx0/sars_cov2/'+table+'/'+hadoopfilename])
	print('Refreshing {}'.format(table))
	run([himpala, 'refresh {}'.format(table), 'sars_cov2'])

loadHadoop(bbdukstats, 'primer_trimming', '{}_bbdukstats.txt'.format(config['runid']))
loadHadoop(irmaReadStats, 'irmareadcounts', '{}_{}.txt'.format(config['machine'], config['runid']))
loadHadoop(ampCov, 'amplicon_coverage', '{}_amplicon_coverage.txt'.format(config['runid']))
loadHadoop(irmaIns, 'cdc_irma_insertions', '{}_insertions.txt'.format(config['runid']))
loadHadoop(irmaDel, 'cdc_irma_deletions', '{}_deletions.txt'.format(config['runid']))
loadHadoop(irmaCov, 'cdc_irma_coverage', '{}_coverage.txt'.format(config['runid']))
loadHadoop(irmaAll, 'cdc_irma_allalleles', '{}_allalleles.txt'.format(config['runid']))
loadHadoop(irmaConsensus, 'cdc_production_all', '{}_consensus.txt'.format(config['runid']))
loadHadoop(daisIns, 'alignment_insertions', '{}.ins'.format(config['runid']))
loadHadoop(daisDel, 'alignment_deletions', '{}.del'.format(config['runid']))
loadHadoop(daisSeq, 'alignments', '{}.seq'.format(config['runid']))
loadHadoop(daisGenIns, 'genome_insertions', '{}.gen.ins'.format(config['runid']))
loadHadoop(daisGen, 'genomes', '{}.gen'.format(config['runid']))
loadHadoop(daisGenDel, 'genome_deletions', '{}.gen.del'.format(config['runid']))
loadHadoop(benchmark, 'snakemake_benchmarks', '{}_{}.txt'.format(config['machine'], config['runid']))
for f in config_parquet:
    loadHadoop(f, 'cdc_config', f)
