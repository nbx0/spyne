import yaml
from glob import glob
from subprocess import run
from os.path import realpath, dirname
import pandas as pd

spath = dirname(__file__)
himpala = spath+'/himpala'
hput = spath+'/hput'

# snakemake config 2 dict
with open('config.yaml','r') as d:
	config = yaml.safe_load(d)
machine = config['machine']
runid = config['runid']

# creation_date
with open('hadoop/{}_consensus.txt'.format(runid), 'r') as d:
	creation_date = d.readline().strip().split('\t')[-1]

# irma config 2 dict
irma_config = {'machine':machine, 'runid':runid, 'creation_date':creation_date}
with open(glob('IRMA/*/logs/run_info.txt')[0], 'r') as d:
	for line in d:
		l = line.strip().split('\t')
		try:
			irma_config[l[0]] = l[2]
		except IndexError:
			l = line.split()
			irma_config[l[0]] = l[2]

for i in ['machine','runid','creation_date','program_name','program_version','last_git_commit_hash','sample','paired_end_reads','data','module_name','module_param_call','parameter_file_name','parameter_file_version','match_last_program','align_last_program','sort_last_program','align_last_deletion_type','assemble_last_program','match_programs','sort_programs','align_programs','deletion_types','blat_identity','minimum_blat_match_length','profiles','do_not_merge_read_pairs','starting_reference','grid_acceleration_on','grid_optional_path','working_directory','alternative_frequency','alternative_count','skip_reference_elongation','read_statistic','minimum_statistic_quality','minimum_read_length','adapter_trim_read_motif','adapter_allow_one_mismatch','enforce_clipped_length','interval_significance_level','maximum_read_gathering_rounds','read_fasta_input','minimum_read_patterns','minimum_read_patterns_residual','minimum_reads','minimum_reads_residual','match_to_altmatch_ratio','minimum_insertion_edit_threshold','minimum_deletion_edit_threshold','minimum_insertion_edit_depth','minimum_deletion_edit_depth','silence_complex_indels_for_editing','minimum_frequency_for_mixed_consensus_call','minimum_consensus_support','minimum_consensus_average_quality','auto_adjust_minimum_variant_frequency','minimum_deletion_variant_frequency','minimum_insertion_variant_frequency','minimum_variant_frequency','minimum_variant_count','minimum_variant_average_quality','minimum_variant_depth','minimum_confidence_not_sequencer_error','merge_secondary_data','do_secondary_assembly','final_assembly_to_reference_seed']:
    if i not in irma_config.keys():
        irma_config[i] = 'Null'

irma_configDF = pd.DataFrame(irma_config, index=[0])

timestamp = creation_date.replace(" ","_").replace("-","").replace(":","")

with open('hadoop/{}_{}_config.txt'.format(runid,timestamp), 'w') as out:
    irma_configDF.to_csv(out,sep='\t',header=False,index=False)


def loadHadoop(file, table, hadoopfilename=''):
	if not isinstance(file, list):
			file = [file]
	for f in file:
		if hadoopfilename == '':
			hadoopfilename = f
		print('Loading {} to /user/nbx0/sars_cov2/{}/{}'.format(f, table, hadoopfilename))
		run([hput, f, '/user/nbx0/sars_cov2/'+table+'/'+hadoopfilename])

loadHadoop('hadoop/{}_{}_config.txt'.format(runid,timestamp), 'cdc_config', '{}_{}_config.txt'.format(runid,timestamp))

cmd = himpala+' "insert into cdc_config values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\'); refresh cdc_config;" sars_cov2'.format(
	irma_config['machine'] ,
	irma_config['runid'] ,
	irma_config['creation_date'] ,
	irma_config['program_name'] ,
	irma_config['program_version'] ,
	irma_config['last_git_commit_hash'] ,
	irma_config['sample'] ,
	irma_config['paired_end_reads'] ,
	irma_config['data'] ,
	irma_config['module_name'] ,
	irma_config['module_param_call'] ,
	irma_config['parameter_file_name'] ,
	irma_config['parameter_file_version'] ,
	irma_config['match_last_program'] ,
	irma_config['align_last_program'] ,
	irma_config['sort_last_program'] ,
	irma_config['align_last_deletion_type'] ,
	irma_config['assemble_last_program'] ,
	irma_config['match_programs'] ,
	irma_config['sort_programs'] ,
	irma_config['align_programs'] ,
	irma_config['deletion_types'] ,
	irma_config['blat_identity'] ,
	irma_config['minimum_blat_match_length'] ,
	irma_config['profiles'] ,
	irma_config['do_not_merge_read_pairs'] ,
	irma_config['starting_reference'] ,
	irma_config['grid_acceleration_on'] ,
	irma_config['grid_optional_path'] ,
	irma_config['working_directory'] ,
	irma_config['alternative_frequency'] ,
	irma_config['alternative_count'] ,
	irma_config['skip_reference_elongation'] ,
	irma_config['read_statistic'] ,
	irma_config['minimum_statistic_quality'] ,
	irma_config['minimum_read_length'] ,
	irma_config['adapter_trim_read_motif'] ,
	irma_config['adapter_allow_one_mismatch'] ,
	irma_config['enforce_clipped_length'] ,
	irma_config['interval_significance_level'] ,
	irma_config['maximum_read_gathering_rounds'] ,
	irma_config['read_fasta_input'] ,
	irma_config['minimum_read_patterns'] ,
	irma_config['minimum_read_patterns_residual'] ,
	irma_config['minimum_reads'] ,
	irma_config['minimum_reads_residual'] ,
	irma_config['match_to_altmatch_ratio'] ,
	irma_config['minimum_insertion_edit_threshold'] ,
	irma_config['minimum_deletion_edit_threshold'] ,
	irma_config['minimum_insertion_edit_depth'] ,
	irma_config['minimum_deletion_edit_depth'] ,
	irma_config['silence_complex_indels_for_editing'] ,
	irma_config['minimum_frequency_for_mixed_consensus_call'] ,
	irma_config['minimum_consensus_support'] ,
	irma_config['minimum_consensus_average_quality'] ,
	irma_config['auto_adjust_minimum_variant_frequency'] ,
	irma_config['minimum_deletion_variant_frequency'] ,
	irma_config['minimum_insertion_variant_frequency'] ,
	irma_config['minimum_variant_frequency'] ,
	irma_config['minimum_variant_count'] ,
	irma_config['minimum_variant_average_quality'] ,
	irma_config['minimum_variant_depth'] ,
	irma_config['minimum_confidence_not_sequencer_error'] ,
	irma_config['merge_secondary_data'] ,
	irma_config['do_secondary_assembly'] ,
	irma_config['final_assembly_to_reference_seed'])
c = run([cmd], shell=True, capture_output=True)
if c.returncode != 0:
    print(c.stderr)

