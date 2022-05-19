#!/bin/bash
# K. Lacek
# May 17 2022

SCRIPT_PATH="/scicomp/groups-pure/sars2seq/dev/on-premises-ont-assembly/scripts"
LIST_FILE="$SCRIPT_PATH/config/instruments_list.txt"
ARTIFACT_LOG="$SCRIPT_PATH/logs/runids_processed.log"
INSTRUMENTS_GWAS="/scicomp/instruments"

file_last_modified() {
    date -d "now - $( stat -c "%Y" $1 ) seconds" +%s
}

if ! [ -d "$SCRIPT_PATH/logs" ]; then
    mkdir $SCRIPT_PATH/logs
fi

TIME_FILTER=86400 # 24 h default initial search unless provided or set via log
if [[ $TIME_FILTER_INPUT ]]; then
    TIME_FILTER=$TIME_FILTER_INPUT
elif [ -e $ARTIFACT_LOG ]; then
    TIME_FILTER=$(file_last_modified $ARTIFACT_LOG)
    ((TIME_FILTER+=300)) # Extra padding of 5 mins
fi


if [ -e $LIST_FILE ] && [[ $TIME_FILTER ]]; then

    echo -e "\n[$(date '+%F %T')]\n...Searching for files created in last $(( TIME_FILTER / 60)) mins"

    for INSTR in $(cat $LIST_FILE | xargs)
    do 
        for INSTRUMENTS_GWA in $INSTRUMENTS_GWAS
        do
	    INSTR_DIR=$INSTRUMENTS_GWA/$INSTR
            if [ -d $INSTR_DIR ]; then
                echo "...Checking Instrument Directory $INSTR_DIR"
                LATEST_DIR=$(ls -dt $INSTR_DIR/* | head -n 1 )
		echo "...Latest finished run found at $LATEST_DIR"
		SEQ_SUM=$LATEST_DIR/*/*/sequencing_summary*.txt
		if [ ! -z $SEQ_SUM ]; then
			echo "...Sequencing summary found at $SEQ_SUM"
                    if (( $(file_last_modified $SEQ_SUM) < $TIME_FILTER )); then
                        RUNFOLDER=$LATEST_DIR
                        echo "...Run Complete indicator located...RUN FOLDER = $RUNFOLDER"
                        # Run instrument integration wrapper for completed run
                        #$SCRIPT_PATH/ilmn_wrapper.sh -s $CLARITY_HOSTNAME -u $APIUSER -p $CRED -r $RUNFOLDER
			echo "...Copying run $(basename $RUNFOLDER)"
			cp -r $RUNFOLDER /scicomp/groups-pure/sars2seq/data/by-instrument/$INSTR/ && touch /scicomp/groups-pure/sars2seq/data/by-instrument/$INSTR/$(basename $RUNFOLDER)/demux.fin
                    fi
                fi
            fi
        done
    done

elif ! [ -e $LIST_FILE ]; then
    echo -e "\nusage:\n$USAGE\n\nInstruments list file ($LIST_FILE) not found in this directory"
fi

