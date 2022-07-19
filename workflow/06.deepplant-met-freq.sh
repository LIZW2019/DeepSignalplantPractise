#06.deepplant-met-freq.sh
#environment setting, replace $CondaEnv/deepsignalpenv with your actual path
export PATH=/public/home/lizw/anaconda3/envs/deepsignalpenv/bin:$PATH
#calculate frequency
deepsignal_plant call_freq \
--input_path ../cache/SINGLE_sample_data/fast5s.C.call_mods.tsv \
--result_file ../cache/SINGLE_sample_data/fast5s.C.call_mods.freq.bed \
--sort --bed
