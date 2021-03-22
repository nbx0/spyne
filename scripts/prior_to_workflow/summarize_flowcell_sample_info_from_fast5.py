#!/usr/bin/env python3


import argparse
import os
import sys
import warnings


def parse_args():
    parser = argparse.ArgumentParser(description="Summarizes run information "
        "from a Fast5 file", add_help=False)
    req = parser.add_argument_group("Required")
    req.add_argument("-i", "--infile", required=True, metavar="FILE",
        help="input Fast5 file")
    opt = parser.add_argument_group("Optional")
    opt.add_argument("-c", "--cell", metavar="FILE", type=str,
        help="create script to enable fetching additional ??????????"
        " depends on kitcell.py [off]")
    opt.add_argument("-h", "--help", action="help",
        help="show this help message and exit")
    opt.add_argument("-o", "--outfile", metavar="FILE", type=str,
        help="tab-delimited output file [stdout]")
    return parser.parse_args()


def main():
    opt = parse_args()
    infile = os.path.realpath(os.path.expanduser(opt.infile))

    with warnings.catch_warnings(): #suppresses FutureWarning from h5py import
        warnings.simplefilter("ignore")
        import h5py

    d = {}
    with h5py.File(infile, "r") as f:
        # http://docs.h5py.org/en/stable/quick.html
        d['device_id'] = f[list(f.keys())[1]]["tracking_id"].attrs["device_id"] #e.g., 'X5'
        d['flow_cell_id'] = f[list(f.keys())[1]]["tracking_id"].attrs["flow_cell_id"] #e.g., 'FAP52730'
        d['flow_cell_product_code'] = f[list(f.keys())[0]]["tracking_id"].attrs["flow_cell_product_code"] #e.g., 'FLO-MIN106'
        d['sequencing_kit'] = f[list(f.keys())[1]]["context_tags"].attrs["sequencing_kit"].upper() #e.g., 'sqk-lsk109'

        # misc data we might be interested in logging later
        d['guppy_ver'] = f[list(f.keys())[1]]["tracking_id"].attrs["guppy_version"] #e.g., '4.2.3+f90bd04'
        d['protocol_group_id'] = f[list(f.keys())[1]]["tracking_id"].attrs["protocol_group_id"] #e.g., 'E0211-nCoV_031121'
        d['run_hash'] = f[list(f.keys())[1]]["tracking_id"].attrs["run_id"] #e.g., 'c11fd37ee5674c0f0dcf8875ce94bb29f8852d20'
        d['sample_id'] = f[list(f.keys())[1]]["tracking_id"].attrs["sample_id"] #e.g., 'no_sample'
        d['protocol_run_hash'] = f[list(f.keys())[1]]["tracking_id"].attrs["protocol_run_id"] #e.g., 'ea413d91-9e92-4db6-857c-87f02fa9facb'
        d['experiment_type'] = f[list(f.keys())[1]]["context_tags"].attrs["experiment_type"] #e.g., 'genomic_dna'

    d = {k:str((v).decode('UTF-8')) for k, v in d.items()}

    # NOTE: we can form outfile structure with above data if we could find a
    #  way to pull out the <barcodeINT> from within the Fast5 file
    #  e.g., 'FAP52730_pass_barcode01_c11fd37e_11.fast5'
    #  and   'FAP52730_pass_barcode01_c11fd37e_11.fastq'
    #  are formed with <flow_cell_id>, <barcodeINT>, and <first 8 char of run_hash>
    # hash_prefix = d['run_hash'][0:8]
    # seqfile_regex = '{}_pass_{}_{}_*.fast*'.format( d['flow_cell_id'], 'barcodeINT', hash_prefix)
    # print('file regex is: {}'.format(seqfile_regex))

    # Do we want to report any more info that this?
    o = [" \t".join(
            [d['device_id'], d['flow_cell_id'],
            d['flow_cell_product_code'], d['sequencing_kit']])]

    if opt.cell is not None:
        # TO-DO: ask Ben
        cell = os.path.realpath(os.path.expanduser(opt.cell))
        print('@Ben, what should this option invoke? Just print py script or'
        ' actually run the py script and produce the output?')
        # with open(sys.argv[3]+'kitcell.py', 'a+') as o:
        #     print("#!/usr/bin/env python", "seqKit = '"+sequencing_kit+"'", "flow_cell_id = '"+flow_cell_product_code+"'","runID = '"+run_hash+"'", "flowcellID = '"+flowcell+"'", sep='\n',file=o)

    # Write single output file
    if opt.outfile is not None:
        ofh = open(os.path.abspath(os.path.expanduser(opt.outfile)), "w")
    else:
        ofh = sys.stdout
    for ln in o:
        ofh.write("{}\n".format("".join(ln)))

if __name__ == "__main__":
    main()
