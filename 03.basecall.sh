guppy_basecaller \
-i ./SINGLE_sample_data \
-s ./SINGLE_sample_data/fastq \
-c dna_r9.4.1_450bps_hac.cfg \
--recursive \
--disable_pings \
--qscore_filtering \
--device "cuda:all:100%"
