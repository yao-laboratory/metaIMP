bbmap.sh minid=0.9 maxindel=3 bandwidthratio=0.16 bandwidth=12 quickmatch fast minhits=2 \
    ref=/work/yaolab/fernandohq/metaIMP/bbmap/mousecatdoghuman/mm10.fa qtrim=r trimq=10 untrim usemodulo \
    printunmappedcount kfilter=25 maxsites=1 k=14 bloom in1=$fastq1 \
    in2=$fastq2  outu1=$clean1 outu2=$clean2
