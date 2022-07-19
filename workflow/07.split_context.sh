#07.split_context.sh
#replace $PATHofDeepSignalPlant with your actual path
python $PATHofDeepSignalPlant/scripts/split_freq_file_by_5mC_motif.py \
--freqfile ../cache/SINGLE_sample_data/fast5s.C.call_mods.freq.bed \
--ref ../input/reference/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa
