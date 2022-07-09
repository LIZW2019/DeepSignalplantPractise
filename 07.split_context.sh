#07.split_context.sh
python $PATHofDeepSignalPlant/scripts/split_freq_file_by_5mC_motif.py \
--freqfile ./SINGLE_sample_data/fast5s.C.call_mods.freq.bed \
--ref ./reference/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa
