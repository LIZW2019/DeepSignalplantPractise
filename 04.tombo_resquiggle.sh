#04.tombo_resquiggle.sh
#environment setting, replace $CondaEnv/deepsignalpenv with your actual path
export PATH=$CondaEnv/deepsignalpenv/bin:$PATH
# resquiggler
tombo resquiggle \
./SINGLE_sample_data \
./reference/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa.gz \
--processes 30 \
--corrected-group RawGenomeCorrected_000 \
--basecall-group Basecall_1D_000 \
--overwrite \
--ignore-read-locks
