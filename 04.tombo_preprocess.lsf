#environment setting
export PATH=$CondaEnv/deepsignalpenv/bin:$PATH
#main
cat ./SINGLE_sample_data/fastq/pass/*fastq > ./SINGLE_sample_data/fastq/pass.fastq
tombo preprocess annotate_raw_with_fastqs \
--fast5-basedir ./SINGLE_sample_data \
--fastq-filenames ./SINGLE_sample_data/fastq/pass.fastq \
--sequencing-summary-filenames ./SINGLE_sample_data/fastq/sequencing_summary.txt \
--overwrite \
--processes 30
