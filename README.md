# Overview
![](./graphs/pipeline.png)

# Equipment 

Linux version 3.10.0-862.el7.x86_64 (Red Hat 4.8.5-28) with 48 CPU (2*Intel Gold 6140, 18 cores, 2.3 Ghz) and GPU (2*Nvidia V100, 640 cores, 32 GB).

# Installation
The following software shoud be installed according to the guidance in the related protocol.
1.	[Guppy 4.0.0+](https://timkahlke.github.io/LongRead_tutorials/BS_G.html)
2.	[DeepSignal-plant v0.1.5](https://github.com/PengNi/DeepSignal-plant)
* The pipeline of DeepSignal-plant depends on the softwares listed as follow:  
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

# Related scripts
If you clone this repository to your server, you will find a folder named "DeepSignalplantPractise" as an example of the workflow:
```
git clone https://github.com/LIZW2019/DeepSignalplantPractise.git
```
The related scripts are in the folder "DeepSignalplantPractise/lib". 

The script "DeepSignalplantPractise/lib/python_scripts/met_level_bin.py" is used for bin methylation level calculation in Step8.   
The script "DeepSignalplantPractise/lib/python_scripts/chrom_met_visulization.py" is for methylation level distribution plot in Step9. 

The scripts from DeepSignal-plant are expected to be cloned in this folder:
```
cd DeepSignalplantPractise/lib
git clone https://github.com/PengNi/deepsignal-plant.git
```

You will find the script "split_freq_file_by_5mC_motif.py" under the folder "DeepSignalplantPractise/lib/deepsignal-plant/scripts", which will be used in Step7.
We also use $PATHofDeepSignalPlant to indicate the path for Deepsignal-plant download in the code. In this case, $PATHofDeepSignalPlant = "DeepSignalplantPractise/lib/deepsignal-plant/scripts".

# Input Data
The input data should be downloaded into different subfolders under the "DeepSignalplantPractise/input". The data we provided can be access in the our shared Google Drive folder: https://drive.google.com/drive/folders/1XCL6Ovvv9fpjg8A9prgIu2T7Ta5Yjc28

**a.Sequence data in FAST5 format**
Data generated from Nanopore direct DNA sequencing is in FAST5 format.
Sample data for Step1 can be download from the ["Step1_Input" folder in Google Drive](https://drive.google.com/drive/folders/1NZe6mQ5y1S8eaE-GwU124PvmONBoz5X7?usp=sharing).The user can download the file "sample_data.tar.gz" to a local computer and transfer it to the folder "DeepSignalplantPractise/input/Step1_Input". The command below is used to decompress the file:

```
tar -zxvf sample_data.tar.gz 
```

In the decompressed “sample_data” folder, users will find four files ending in .fast5. These example files are in FAST5 format and generated from Nanopore sequencing, containing the raw electric signal that we can call the base sequence and modification. Users can refer to https://hasindu2008.github.io/slow5specs/fast5_demystified.pdf for a detailed introduction of the FAST5 format.

**d.Preprocessed data**
In this case study, some steps would need preprocessed data as input.
In Step3, if you fail to get access to Guppy, you can use our basecalled fastq for the downstream analysis. Download it from the ["Step3_Input" folder in Google Drive](https://drive.google.com/drive/folders/1pk4vecjdC48gslbeXGNKforUb0jxRPpz?usp=sharing) and move it to the "DeepSignalplantPractise/input/Step3_Input".
In Step8, because the sample data is too small for bin calculation and visualization, we provide the preprocessed data from Pore-C as the input. Download it from the ["Step8_Input" folder in Google Drive](https://drive.google.com/drive/folders/14xw6gvQz_gjUi6p86NrSHZq59YABlzZO?usp=sharing) and move it to the "DeepSignalplantPractise/input/Step8_Input".

**b.Reference genome**
Download the reference genome in fasta format for mapping in Step4. Download the Genome gff file and extract the chromosome coordinates for Step8 input.
```
#download reference genome
cd ./DeepSignalplantPractise/input/
mkdir reference
cd reference
wget -c http://ftp.ensemblgenomes.org/pub/plants/release-53/fasta/arabidopsis_thaliana/dna/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa.gz 
gunzip Arabidopsis_thaliana.TAIR10.dna.toplevel.fa.gz

#download gff file
cd ./DeepSignalplantPractise/input/reference
wget -c http://ftp.ensemblgenomes.org/pub/plants/release-53/gff3/arabidopsis_thaliana/Arabidopsis_thaliana.TAIR10.53.gff3.gz 
gunzip Arabidopsis_thaliana.TAIR10.53.gff3.gz
#extract the chromosomes coordinates
awk -F "\t" '{if($3=="chromosome") print($1"\t"$4-1"\t"$5)}' Arabidopsis_thaliana.TAIR10.53.gff3 > Tair10_genome.bed
```

**c.Pretrained model**  
Download the model provided by DeepSignal-plant on its GitHub page (https://github.com/PengNi/DeepSignal-plant ) and move it to the folder "DeepSignalplantPractise/input/model" for 5mC calling in Step5.



# Major steps 

In this protocol, we use $PATHofDeepSignalPlant to indicate the path for Deepsignal-plant download and $CondaEnv to indicate the path of the Conda environment. Users will need to replace these two variables manually with the path they use.

**Step1. Convert the multi-read FAST5 into single-read form**
```
#01.multi_to_single_fast5.sh
multi_to_single_fast5 -i ../input/Step1_Input/sample_data -s ../cache/SINGLE_sample_data/ -t 30 --recursive
```

**Step2. Basecall FAST5 files with Guppy**

```
#02.basecall.sh
guppy_basecaller \
-i ../cache/SINGLE_sample_data/ \
-s ../cache/SINGLE_sample_data/fastq \
-c dna_r9.4.1_450bps_hac_prom.cfg \
--recursive \
--disable_pings \
--qscore_filtering \
--device "cuda:all:100%"
```

**Step3. Add the basecalled sequence back to FAST5 with Tombo preprocess**

```
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
```
**Step4. Map the raw signal to reference genome with Tombo resquiggle**

```
#04.tombo_resquiggle.sh
#environment setting, replace $CondaEnv/deepsignalpenv with your actual path
export PATH=$CondaEnv/deepsignalpenv/bin:$PATH
# resquiggler
tombo resquiggle \
../cache/SINGLE_sample_data/ \
../input/reference/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa \
--processes 30 \
--corrected-group RawGenomeCorrected_000 \
--basecall-group Basecall_1D_000 \
--overwrite \
--ignore-read-locks
```

**Step5. Call methylation of reads with DeepSignal-plant call_mods**
```
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
```

**Step6. Calculate methylation frequency with DeepSignal-plant call_freq**
```
#06.deepplant-met-freq.sh
#environment setting, replace $CondaEnv/deepsignalpenv with your actual path
export PATH=$CondaEnv/deepsignalpenv/bin:$PATH
#calculate frequency
deepsignal_plant call_freq \
--input_path ../cache/SINGLE_sample_data/fast5s.C.call_mods.tsv \
--result_file ../cache/SINGLE_sample_data/fast5s.C.call_mods.freq.bed \
--sort --bed
```

**Step7. Split the result into CG, CHG, and CHH context**
```
#07.split_context.sh
#replace $PATHofDeepSignalPlant with your actual path
python $PATHofDeepSignalPlant/scripts/split_freq_file_by_5mC_motif.py \
--freqfile ../cache/SINGLE_sample_data/fast5s.C.call_mods.freq.bed \
--ref ../input/reference/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa
```

**Step8. Calculate the weighted methylation level in the bin**

```
#08.met_level_bin.sh
python ../lib/python_scripts/met_level_bin.py \
--region_bed ../input/reference/Tair10_genome.bed \
--met_bed ../input/Step8_Input/porec_rep2/forstep08/Rep2_fast5s.C.call_mods.CG.frequency.bed \
--prefix Rep2_fast5s.C.call_mods.CG \
--binsize 100000 \
--outdir ../output
```

**Step9. Visualize the methylation level by IGV and python plotting**

```
#09.chrom_met_visulization.sh
python ../lib/python_scripts/chrom_met_visulization.py \
--cg_bedg ../output/Rep2_fast5s.C.call_mods.CG_binsize100000.bedgraph \
--chg_bedg ../output/Rep2_fast5s.C.call_mods.CHG_binsize100000.bedgraph \
--chh_bedg ../output/Rep2_fast5s.C.call_mods.CHH_binsize100000.bedgraph \
--region_bed ../input/reference/Tair10_genome.bed \
--chrom 4 --outdir ../output
```

# Expected results
**The intermediate results and the final results of this workflow is large, so we keep only part of the files as examples under the folder "cache" and "output" respectively, with the name marked with "EXAMPLE".**


* IGV 
![](./graphs/IGV.png)

* python plot
![](./graphs/Chr4_methylation_distribution.png)
