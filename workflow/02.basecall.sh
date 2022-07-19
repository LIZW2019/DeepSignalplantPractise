#02.basecall.sh
guppy_basecaller \
-i ../cache/SINGLE_sample_data/ \
-s ../cache/SINGLE_sample_data/fastq \
-c dna_r9.4.1_450bps_hac_prom.cfg \
--recursive \
--disable_pings \
--qscore_filtering \
--device "cuda:all:100%"
