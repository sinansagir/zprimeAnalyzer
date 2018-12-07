for job in `seq  37413 37452`; do 
	condor_rm $job 
done
