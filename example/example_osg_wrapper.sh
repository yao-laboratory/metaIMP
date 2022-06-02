#!/bin/bash

EXPECTED_ARGS=6

if [ $# -ne $EXPECTED_ARGS ]; then
	 echo "Usage: metaimp testing"
	 exit 1
else
	 source activate metaimp_env3
	 /home/yaolab/ksahu2/.ssh/metaIMP/main_assembly_processing.sh $1 $2 $3 $4 $5 $6
	 conda deactivate
fi
	
