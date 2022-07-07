#environment setting
export PATH=$CondaEnv/deepsignalpenv/bin:$PATH
#main
export PATH=$CondaEnv/deepsignalpenv/bin:$PATH
CUDA_VISIBLE_DEVICES=0,1 deepsignal_plant call_mods \
--input_path ./SINGLE_sample_data \
--model_path ./model/model.dp2.CNN.arabnrice2-1_120m_R9.4plus_tem.bn13_sn16.both_bilstm.epoch6.ckpt \
--result_file ./SINGLE_sample_data/fast5s.C.call_mods.tsv \
--corrected_group RawGenomeCorrected_000 \
--reference_path ./reference/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa.gz \
--motifs C --nproc 30 --nproc_gpu 2--ignore-read-locks
