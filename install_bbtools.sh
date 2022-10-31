
#!/bin/bash
# Wrapper to install downloaded packages 

PACKAGE_ROOT=/opt/bbtools
RESOURCE_ROOT=/SC2-spike-seq
bbtools_orig=${RESOURCE_ROOT}/bbtools/bbtools_file.txt
bbtools_clean=${RESOURCE_ROOT}/bbtools/bbtools_file_clean.txt

# Make the bbtools directory exits, if not, create it
if [[ ! -d ${PACKAGE_ROOT} ]]
then
	mkdir ${PACKAGE_ROOT}
fi

# Extract bbmap package to the bbtools directory
if [[ -f ${bbtools_orig} ]]
then

	echo "Install bbtools"

	# Remove blank lines from the file and save a cleaner version of it
	awk NF < ${bbtools_orig} > ${bbtools_clean}

	# Get number of rows in bbtools_file_clean.txt
	n=`wc -l < ${bbtools_clean}`
	i=1

	# Wget the file and install the package
	while [[ i -le $n ]];
	do
		echo $i
		file=$(head -${i} ${bbtools_clean} | tail -1 | sed 's,\r,,g')
		echo $file
		sudo tar -zxf ${RESOURCE_ROOT}/bbtools/${file} -C ${PACKAGE_ROOT}
		i=$(($i+1))
	done

	# return message to keep the process going
	echo "Done"

fi