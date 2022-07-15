# Overview
![](https://i.bmp.ovh/imgs/2022/07/15/a391a1e5c274bdf7.png)

# Equipment 

Linux version 3.10.0-862.el7.x86_64 (Red Hat 4.8.5-28) with 48 CPU (2*Intel Gold 6140, 18 cores, 2.3 Ghz) and GPU (2*Nvidia V100, 640 cores, 32 GB).

# Installation
1.	[Guppy 4.0.0+](https://timkahlke.github.io/LongRead_tutorials/BS_G.html)
2.	[DeepSignal-plant v0.1.5](https://github.com/PengNi/DeepSignal-plant)
* The pipeline for DeepSignal-plant depends on software listed as follow:  
  a.	[ont_fast5_api v4.0.2](https://github.com/nanoporetech/ont_fast5_api)  
  b.	[tombo v1.5.1](https://github.com/nanoporetech/tombo)  
  c.	[Conda v4.9.2](https://docs.conda.io/en/latest/)  
h5ls tools we use to preview the FAST5 files would be installed automatically with conda.
4.  [The Integrative Genomics Viewer (IGV) v2.6.1](https://software.broadinstitute.org/software/igv/)
5.  [Python 3.7.12](https://www.python.org/)
	* [Numpy v1.20.3](https://numpy.org/)
	* [Pandas v1.3.4](https://pandas.pydata.org/)
	* [Click v8.1.3](https://click.palletsprojects.com/en/8.1.x/)
	* [Seaborn v0.11.1](https://seaborn.pydata.org/)
	* [Matplotlib v3.4.1](https://matplotlib.org/)
	* [hurry.filesize 0.9](https://pypi.org/project/hurry.filesize/)

# Input Data

**1.Sequence data in FAST5 format**
Data generated from Nanopore direct DNA sequencing in FAST5 format.
Sample data can be download from the google device:   
https://drive.google.com/drive/folders/1XCL6Ovvv9fpjg8A9prgIu2T7Ta5Yjc28?usp=sharing

The user can download it to a local computer and transfer it to the server under the folder clone for this practice. The command below is used to decompress the file:

```
tar -zxvf sample_data.tar.gz 
```

In the “sample_data” folder, users will find four files ending in .fast5. These example files are in FAST5 format and generated from Nanopore sequencing, containing the raw electric signal that we can call the base sequence and modification. Users can refer to https://hasindu2008.github.io/slow5specs/fast5_demystified.pdf for a detailed introduction of the FAST5 format.

**2.Reference genome**
Reference genome in fasta format for mapping in Step4. Genome gff file should be downloaded and the chromosome coordinates are extracted for Step 8 input.
```
cd DeepSignalplantPractise
mkdir reference
cd reference
wget -c http://ftp.ensemblgenomes.org/pub/plants/release-53/fasta/arabidopsis_thaliana/dna/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa.gz 
gunzip Arabidopsis_thaliana.TAIR10.dna.toplevel.fa.gz
wget -c http://ftp.ensemblgenomes.org/pub/plants/release-53/gff3/arabidopsis_thaliana/Arabidopsis_thaliana.TAIR10.53.gff3.gz 
gunzip Arabidopsis_thaliana.TAIR10.53.gff3.gz
#extract the chromosomes coordinates
awk -F "\t" '{if($3=="chromosome") print($1"\t"$4-1"\t"$5)}' Arabidopsis_thaliana.TAIR10.53.gff3 > Tair10_genome.bed
```

**3.Pretrain model**  
Download the model provided by DeepSignal-plant and move it to a new created folder "model" for 5mC calling in sStep5.

# Major steps 

In this protocol, we use $PATHofDeepSignalPlant to indicate the path for Deepsignal-plant download and $CondaEnv to indicate the path of the Conda environment. Users will need to replace these two variables manually with the path they use.

**Step1. Convert the multi-read FAST5 into single-read form**
```
#01.multi_to_single_fast5.sh
multi_to_single_fast5 -i ./sample_data -s ./SINGLE_sample_data -t 30 --recursive
```

**Step2. Basecall FAST5 files with Guppy**

```
#02.basecall.sh
guppy_basecaller \
-i ./SINGLE_sample_data \
-s ./SINGLE_sample_data/fastq \
-c dna_r9.4.1_450bps_hac_prom.cfg \
--recursive \
--disable_pings \
--qscore_filtering \
--device "cuda:all:100%"
```

**Step3. Add the basecalled sequence back to FAST5 with Tombo preprocess**

```
#03.tombo_preprocess.sh
#environment setting, replace $CondaEnv/deepsignalpenv with actual path
export PATH=$CondaEnv/deepsignalpenv/bin:$PATH
# Tombo preprocess
cat ./SINGLE_sample_data/fastq/pass/*fastq > ./SINGLE_sample_data/fastq/pass.fastq
tombo preprocess annotate_raw_with_fastqs \
--fast5-basedir ./SINGLE_sample_data \
--fastq-filenames ./SINGLE_sample_data/fastq/pass.fastq \
--sequencing-summary-filenames ./SINGLE_sample_data/fastq/sequencing_summary.txt \
--overwrite \
--processes 30
```
**Step4. Map the raw signal to reference genome with Tombo resquiggle**

```
#04.tombo_resquiggle.sh
#environment setting, replace $CondaEnv/deepsignalpenv with actual path
export PATH=$CondaEnv/deepsignalpenv/bin:$PATH
# resquiggler
tombo resquiggle \
./SINGLE_sample_data \
/reference/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa.gz \
--processes 30 \
--corrected-group RawGenomeCorrected_000 \
-basecall-group Basecall_1D_000 \
--overwrite \
--ignore-read-locks
```

**Step5. Call methylation of reads with DeepSignal-plant call_mods**
```
#05.deepplant-met-mod.sh
#environment setting, replace $CondaEnv/deepsignalpenv with actual path
export PATH=$CondaEnv/deepsignalpenv/bin:$PATH
#call 5mC
CUDA_VISIBLE_DEVICES=0,1 deepsignal_plant call_mods \
--input_path ./SINGLE_sample_data \
--model_path ./model/model.dp2.CNN.arabnrice2-1_120m_R9.4plus_tem.bn13_sn16.both_bilstm.epoch6.ckpt \
--result_file ./SINGLE_sample_data/fast5s.C.call_mods.tsv \
--corrected_group RawGenomeCorrected_000 \
--reference_path ./reference/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa \
--motifs C --nproc 30 --nproc_gpu 2
```

**Step6. Calculate methylation frequency with DeepSignal-plant call_freq**
```
#06.deepplant-met-freq.sh
#environment setting, replace $CondaEnv/deepsignalpenv with actual path
export PATH=$CondaEnv/deepsignalpenv/bin:$PATH
#calculate frequency
deepsignal_plant call_freq \
--input_path ./SINGLE_sample_data/fast5s.C.call_mods.tsv \
--result_file ./SINGLE_sample_data/fast5s.C.call_mods.freq.bed \
--sort --bed
```

**Step7. Split the result into CG, CHG, and CHH context**
```
#07.split_context.sh
python $PATHofDeepSignalPlant/scripts/split_freq_file_by_5mC_motif.py \
--freqfile ./SINGLE_sample_data/fast5s.C.call_mods.freq.bed \
--ref ./reference/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa
```

**Step8. Calculate the weighted methylation level in the bin**

```
#08.met_level_bin.sh
python python_scripts/met_level_bin.py \
--region_bed reference/Tair10_genome.bed \
--met_bed Rep2_fast5s.C.call_mods.CG.frequency.bed \
--prefix Rep2_fast5s.C.call_mods.CG \
--binsize 100 \
--outdir ./
```

**Step9. Visualize the methylation level by IGV and python plotting**

```
#09.chrom_met_visulization.sh
python python_scripts/chrom_met_visulization.py \
--cg_bedg Rep2_fast5s.C.call_mods.CG_binsize100000.bedgraph \
--chg_bedg Rep2_fast5s.C.call_mods.CHG_binsize100000.bedgraph \
--chh_bedg Rep2_fast5s.C.call_mods.CHH_binsize100000.bedgraph \
--region_bed reference/Tair10_genome.bed \
--chrom 4 --outdir .
```

# Expected results
* IGV
![](https://i.bmp.ovh/imgs/2022/07/15/6926219c876358d3.png)

* python plot
![](https://s3.bmp.ovh/imgs/2022/07/15/2d6b39652145e048.png)
