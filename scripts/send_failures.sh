#!/bin/bash

while getopts ':i:a:c:r:' OPTION
do
	case $OPTION in
	i ) INPUT="$OPTARG";; #comma-delim samples that failed
	a ) ADDR="$OPTARG";; #comma-delim email addresses
	c ) CCADDR="$OPTARG";; #comma-delim cc email addresses
	r ) RUNID="$OPTARG";;
		esac
done
BODY=$(echo $INPUT | sed -s 's/,/\t/g')  
HEADER="Barcode\tCSID_CUID\tClarity_ID\n"
(

echo "Subject: Failed samples found in GridION output of run $RUNID"
echo "From: SC2genomics@mail.biotech.cdc.gov"

echo "To: $ADDR"

echo "Cc: $CCADDR"

echo "Content-type: text/html"

echo

               awk -F $'\t' 'BEGIN{print "<table>"} {print "<tr>"; if (NR==1) { print "<b>"; for(i=1;i<=NF;i++)print "<td>" $i"</td>"; print "</b>" } else { for(i=1;i<=NF;i++)print "<td>" $i"</td>" };print  "</tr>"} END{print "</table>"}' <( echo -e "$HEADER$BODY" )      ) | sendmail -t


