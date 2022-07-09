#06.deepplant-met-freq.sh
#environment setting, replace $CondaEnv/deepsignalpenv with your actual path
export PATH=$CondaEnv/deepsignalpenv/bin:$PATH
#calculate frequency
deepsignal_plant call_freq \
--input_path ./SINGLE_sample_data/fast5s.C.call_mods.tsv \
--result_file ./SINGLE_sample_data/fast5s.C.call_mods.freq.bed \
--sort --bed
