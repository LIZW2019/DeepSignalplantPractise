#05.deepplant-met-mod.sh
#environment setting, replace $CondaEnv/deepsignalpenv with your actual path
export PATH=$CondaEnv/deepsignalpenv/bin:$PATH
#call 5mC
CUDA_VISIBLE_DEVICES=0,1 deepsignal_plant call_mods \
--input_path ../cache/SINGLE_sample_data \
--model_path ../input/model/model.dp2.CNN.arabnrice2-1_120m_R9.4plus_tem.bn13_sn16.both_bilstm.epoch6.ckpt \
--result_file ../cache/SINGLE_sample_data/fast5s.C.call_mods.tsv \
--corrected_group RawGenomeCorrected_000 \
--reference_path ../input/reference/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa \
--motifs C --nproc 30 --nproc_gpu 2
