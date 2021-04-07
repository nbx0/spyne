import yaml
from glob import glob
from datetime import datetime
import pandas as pd
from pyspark.sql import SparkSession

# snakemake config 2 dict
with open('config.yaml','r') as d:
    config = yaml.safe_load(d)
machine = config['machine']
runid = config['runid']
try:
    runid_file = config['runid_file']
except:
    runid_file = config['runid']

# Put top-level key:value pairs into key=header dictionary for proper impala mapping in hadoop
del_list = []
for k,v in config.items():
	if not isinstance(v, dict):
		config['header'][k] = v
		del_list.append(k)
for k in del_list:
	del(config[k])

# irma config 2 dict
irma_config = {}
with open(glob('IRMA/*/logs/run_info.txt')[0], 'r') as d:
    for line in d:
        l = line.strip().split('\t')
        try:
            irma_config[l[1]] = l[2]
        except IndexError:
            l = line.split()
            irma_config[l[1]] = l[2]

# data for spark dataframe conversion
data = [(machine, runid,  datetime.now().strftime('%Y-%m-%d %H:%M:%S'), config, irma_config)]

# generic spark session
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

df = spark.createDataFrame(data, ["machine", "runid", "creation_date", "snakemake_config", "irma_config"])

df.write.parquet('hadoop/parquet/', mode='overwrite')
