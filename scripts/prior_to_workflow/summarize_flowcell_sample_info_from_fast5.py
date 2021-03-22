#!/usr/bin/python3

# Works with multiread fast5

from sys import argv, exit
import warnings
with warnings.catch_warnings(): # To suppress annoying FutureWarning from h5py import
	warnings.simplefilter('ignore')
	import h5py

if len(argv) < 2:
	exit('\n    USAGE: '+argv[0]+' <readfile.fast5>\n')
with h5py.File(argv[1], 'r') as f:
	machine = str(f[list(f.keys())[1]]['tracking_id'].attrs['device_id']).split("'")[1].upper()
	flowcell = str(f[list(f.keys())[1]]['tracking_id'].attrs['flow_cell_id']).split("'")[1].upper()
	flowcell_type = str(f[list(f.keys())[0]]['tracking_id'].attrs['flow_cell_product_code']).split("'")[1].upper()
	seq_kit = str(f[list(f.keys())[1]]['context_tags'].attrs['sequencing_kit']).split("'")[1].upper()
	runID = str(f[list(f.keys())[1]]['tracking_id'].attrs['run_id']).split("'")[1].upper()

if '-c' in argv:
	#try:
	with open(argv[3]+'kitcell.py', 'a+') as o:
		print("#!/usr/bin/python", "seqKit = '"+seq_kit+"'", "flowcell = '"+flowcell_type+"'","runID = '"+runID+"'", "flowcellID = '"+flowcell+"'", sep='\n',file=o)
	#except:
	#	exit('\n    *** kitcell.py already exists ***\n\n    USAGE: '+argv[0]+' <readfile.fast5>\n')
else:
	print(machine+'    '+flowcell+'    '+flowcell_type+'    '+seq_kit)
