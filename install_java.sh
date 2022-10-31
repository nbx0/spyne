
#!/bin/bash
# Wrapper to install downloadeded packages 

PACKAGE_ROOT=/opt/java
RESOURCE_ROOT=/SC2-spike-seq
java_orig=${RESOURCE_ROOT}/java/java_file.txt
java_clean=${RESOURCE_ROOT}/java/java_file_clean.txt

# Make the bbtools directory exits, if not, create it
if [[ ! -d ${PACKAGE_ROOT} ]]
then
	mkdir ${PACKAGE_ROOT}
fi

# Extract the java package to the java directory
if [[ -f ${java_orig} ]]
then

	echo "Install java"

	# Remove blank lines from the file and save a cleaner version of it
	awk NF < ${java_orig} > ${java_clean}

	# Get number of rows in java_file_clean.txt
	n=`wc -l < ${java_clean}`
	i=1

	# Wget the file and install the package
	while [[ i -le $n ]];
	do
		echo $i
		file=$(head -${i} ${java_clean} | tail -1 | sed 's,\r,,g')
		directory=$(sed -e 's,open,,g' -e 's,_linux-x64_bin.tar.gz,,g' ${java_clean})
		echo $file
		sudo tar -zxf ${RESOURCE_ROOT}/java/${file} -C ${PACKAGE_ROOT}
		i=$(($i+1))
	done

	# return message to keep the process going
	echo "Done"

fi
