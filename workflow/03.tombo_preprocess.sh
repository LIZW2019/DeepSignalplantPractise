#03.tombo_preprocess.sh
#environment setting, replace $CondaEnv/deepsignalpenv with your actual path
export PATH=$CondaEnv/deepsignalpenv/bin:$PATH
# Tombo preprocess
cat ../cache/SINGLE_sample_data/fastq/pass/*fastq > ../cache/SINGLE_sample_data/fastq/pass.fastq
tombo preprocess annotate_raw_with_fastqs \
--fast5-basedir ../cache/SINGLE_sample_data/ \
--fastq-filenames ../cache/SINGLE_sample_data/fastq/pass.fastq \
--sequencing-summary-filenames ../cache/SINGLE_sample_data/fastq/sequencing_summary.txt \
--overwrite \
--processes 30
