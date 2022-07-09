#03.tombo_preprocess.sh
#environment setting, replace $CondaEnv/deepsignalpenv with your actual path
export PATH=$CondaEnv/deepsignalpenv/bin:$PATH
# Tombo preprocess
cat ./SINGLE_sample_data/fastq/pass/*fastq > ./SINGLE_sample_data/fastq/pass.fastq
tombo preprocess annotate_raw_with_fastqs \
--fast5-basedir ./SINGLE_sample_data \
--fastq-filenames ./SINGLE_sample_data/fastq/pass.fastq \
--sequencing-summary-filenames ./SINGLE_sample_data/fastq/sequencing_summary.txt \
--overwrite \
--processes 30
