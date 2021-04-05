On-premises Oxford Nanopore Technologies (ONT) Data Processing
==============================================================

Analysis from GridION data using the __workflow_basedir__ repository


Processing Results
------------------
# read lengths plot
.. figure:: {{}}/report/{barcodes}.png
   :width: 75%
   :align: center

# depth of coverage across the genome
.. figure:: {{}}/report/IRMA/{barcodes}.png
   :width: 75%
   :align: center


Workflow Summary
----------------
This workflow performs the following steps with :
1. barcode clipping and read cleaning
2. iterative reference-based assembly
3. summarize assembly features and insert into hadoop database


Workflow Graph
--------------
.. figure:: {{}}/report/workflow-graph.png
   :width: 75%
   :align: center


Output Data Structure:
----------------------
.. code-block:: text
  __workflow_workdir__/
  |
  |-- IRMA
  |
  |-- logs
  |   |__ benchmarks
  |
  |-- reports


Versions Used in this Analysis:
-------------------------------

# Docs: https://snakemake.readthedocs.io/en/stable/snakefiles/reporting.html
# Inspired by: NBISweden/manticore-smk report, unsure if it works
