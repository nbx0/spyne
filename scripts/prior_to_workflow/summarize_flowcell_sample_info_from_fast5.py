#!/usr/bin/env python3


import argparse
import sys
import warnings


def parse_args():
    parser = argparse.ArgumentParser(description="Summarizes run information "
        "from a Fast5 file", add_help=False)
    req = parser.add_argument_group("Required")
    req.add_argument("-i", "--infile", required=True, metavar="FILE",
        help="input Fast5 file")
    opt = parser.add_argument_group("Optional")
    opt.add_argument("-c", "--cell", metavar="FILE", type=False,
        help="create script to enable fetching additional ??????????"
        " depends on kitcell.py [off]")
    opt.add_argument("-h", "--help", action="help",
        help="show this help message and exit")
    opt.add_argument("-o", "--outfile", metavar="FILE",
        help="tab-delimited output file [stdout]")
    return parser.parse_args()


def main():
    opt = parse_args()
    infile = os.path.realpath(os.path.expanduser(opt.infile))

    with warnings.catch_warnings(): #suppresses FutureWarning from h5py import
        warnings.simplefilter("ignore")
        import h5py

    with h5py.File(infile, "r") as f:
        machine = str(f[list(f.keys())[1]]["tracking_id"].attrs["device_id"]).split("'")[1].upper()
        flowcell = str(f[list(f.keys())[1]]["tracking_id"].attrs["flow_cell_id"]).split("'")[1].upper()
        flowcell_type = str(f[list(f.keys())[0]]["tracking_id"].attrs["flow_cell_product_code"]).split("'")[1].upper()
        seq_kit = str(f[list(f.keys())[1]]["context_tags"].attrs["sequencing_kit"]).split("'")[1].upper()
        run = str(f[list(f.keys())[1]]["tracking_id"].attrs["run_id"]).split("'")[1].upper()
    o = [s + '\t' for s in (machine, flowcell, flowcell_type, seq_kit, run_id)]


    if opt.cell is not None:
    	cell = os.path.realpath(os.path.expanduser(opt.cell))
        # with open(sys.argv[3]+'kitcell.py', 'a+') as o:
        #     print("#!/usr/bin/env python", "seqKit = '"+seq_kit+"'", "flowcell = '"+flowcell_type+"'","runID = '"+run+"'", "flowcellID = '"+flowcell+"'", sep='\n',file=o)
    
    # Write single output file
    if opt.outfile is not None:
        ofh = open(os.path.abspath(os.path.expanduser(opt.outfile)), "w")
    else:
        ofh = sys.stdout
    for ln in o:
        ofh.write("{}\n".format("".join(ln)))

if __name__ == "__main__":
    main()
