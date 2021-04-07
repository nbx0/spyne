import pandas as pd
from argparse import ArgumentParser as AP
from os.path import realpath, dirname, basename, isfile
from os import stat, remove
from sys import exit
import yaml

def parse_fields(s):
        try:
                h,v = s.split(',')
                return(h,v)
        except:
                raise argparse.ArgumentTypeError("add_fields must be whitespace-seperated list of comma-seperated header,value")


p = AP(description='''Read in text data file(s) and append key-columns''')
r = p.add_argument_group('required arguments')
r.add_argument('-f', '--input_files',  metavar='<inputFiles...>', nargs='+')
r.add_argument('-o', '--output_file', nargs=1)
p.add_argument('-n', '--input_delimiter', help='Default=\'\\t\'', nargs='?', default='\t')
p.add_argument('-u', '--output_delimiter', help='Default=\'\\t\'', nargs='?', default='\t')
p.add_argument('-l', '--add_fields_left', default=[], type=parse_fields, nargs='*',  metavar='<list of header,variable to create additional columns for inputFiles on the LEFT of the dataframe>')
p.add_argument('-r', '--add_fields_right', default=[], type=parse_fields, nargs='*',  metavar='<list of header,variable to create additional columns for inputFiles on the RIGHT of the dataframe>')
#p.add_argument('-p', '--prefix', help='Default=True', action='store_true', default=True)
#p.add_argument('-s', '--suffix', help='Default=False',  action='store_true', default=False)
p.add_argument('--header', help='Default=False', action='store_true', default=False)
p.add_argument('--sc2', action='store_true', default=False, help='Default=False. Extract CUID and CSID from file/paths and prepend to data. Used for DVD\'s SC2 Genomic Analyses Pipeline')
p.add_argument('--benchmark', action='store_true', default=False, help='Default=False. Extract benchmark process name from file/paths and prepend to data. Used for DVD\'s SC2 Genomic Analyses Pipeline')

try:
        args = p.parse_args()
except AttributeError:
        p.print_help()
        exit()
if not args.output_file:
        p.print_help()
        exit()

def findsampleid(filename, config):
        for k in config['barcodes'].keys():
                if k in filename:
                        return k
        if args.benchmark:
                if '_all' in filename:
                        return 'all'

def findbenchmarkprocess(filename):
        for k in ['align2ref', 'amplicov', 'amplicov2hadoop', 'bamsort', 'bbduk', 
                        'bbdukstats2hadoop', 'catallalleles', 'catamplicov', 'catcoverage', 
                        'catdeletions', 'catinsertions', 'checkirma', 'finishup', 'irma', 
                        'irmaconsensus2hadoop', 'irmareads2hadoop', 'irmatables2hadoop', 
                        'realignallalleles', 'realigncoverage', 'realigndeletions', 
                        'realigninsertions', 'subsample']:
                if k in filename:
                        return k

realfiles = []
for f in args.input_files:
        if isfile(f):
                if stat(f).st_size != 0:
                        realfiles.append(f)

if isfile(args.output_file[0]):
        print('removing {}'.format(args.output_file[0]))
        remove(args.output_file[0])

def findvalue(sampleid, field):
        if field in ['machine', 'runid']:
                return config[field]
        elif sampleid == 'all':
                return 'all'
        else:
                return config['barcodes'][sampleid][field]
if args.sc2:
        with open('config.yaml', 'r') as y: #hard code for testing
                config = yaml.safe_load(y)
print(realfiles[0])
if args.benchmark:
        df = pd.read_csv(realfiles[0], sep=args.input_delimiter)
        origCols = df.columns
        df['sampleid'] = findsampleid(realfiles[0], config)
        df['process'] = findbenchmarkprocess(realfiles[0])
        for f in realfiles[1:]:
                df2 = pd.read_csv(f, sep=args.input_delimiter, index_col=False)
                df2['sampleid'] = findsampleid(f, config)
                df2['process'] = findbenchmarkprocess(f)
                df = pd.concat([df, df2])
        for field in ['cuid', 'csid', 'runid', 'machine', 'clarityid', 'Artifactid']:
                df[field] = df['sampleid'].apply(lambda x: findvalue(x, field))
        df = df[['process', 'machine', 'runid', 'csid', 'cuid']+origCols.tolist()+['clarityid', 'Artifactid']]
        if isfile(args.output_file[0]): 
                df.to_csv(args.output_file[0], sep=args.output_delimiter, index=False, header=False, mode='a+')
        else:
                df.to_csv(args.output_file[0], sep=args.output_delimiter, index=False, header=args.header, mode='a+')
else:   
        for f in realfiles:
                df = pd.read_csv(f, sep=args.input_delimiter,index_col=False)
                if args.sc2:
                        sampleid = findsampleid(f, config)
                        if sampleid != 'all':
                                df.insert(loc=0, column='CUID', value=config['barcodes'][sampleid]['cuid'])
                                df.insert(loc=0, column='CSID', value=config['barcodes'][sampleid]['csid'])
                                df.insert(loc=0, column='RUNID', value=config['runid'])
                                df.insert(loc=0, column='MACHINEID', value=config['machine'])
                                df['clarityid'] = config['barcodes'][sampleid]['clarityid']
                                df['Artifactid'] = config['barcodes'][sampleid]['Artifactid']
                for i in args.add_fields_left[::-1]:
                        df.insert(loc=0, column=i[0], value=i[1])
                for i in args.add_fields_right:
                        df[i[0]] = i[1]
                if isfile(args.output_file[0]):
                        df.to_csv(args.output_file[0], sep=args.output_delimiter, index=False, header=False, mode='a+')
                else:
                        df.to_csv(args.output_file[0], sep=args.output_delimiter, index=False, header=args.header, mode='a+')
                        
