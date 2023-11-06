#08.met_level_bin.sh
python ../lib/met_level_bin.py \
--region_bed ../input/reference/Tair10_genome.bed \
--met_bed ../input/Step8_Input/Rep2_fast5s.C.call_mods.CG.frequency.bed \
--prefix Rep2_fast5s.C.call_mods.CG \
--binsize 100000 \
--outdir ../output


python ../lib/met_level_bin.py \
--region_bed ../input/reference/Tair10_genome.bed \
--met_bed ../input/Step8_Input/Rep2_fast5s.C.call_mods.CHG.frequency.bed \
--prefix Rep2_fast5s.C.call_mods.CHG \
--binsize 100000 \
--outdir ../output

python ../lib/met_level_bin.py \
--region_bed ../input/reference/Tair10_genome.bed \
--met_bed ../input/Step8_Input/Rep2_fast5s.C.call_mods.CHH.frequency.bed \
--prefix Rep2_fast5s.C.call_mods.CHH \
--binsize 100000 \
--outdir ../output

