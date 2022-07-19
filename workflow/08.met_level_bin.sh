#08.met_level_bin.sh
python ../lib/python_scripts/met_level_bin.py \
--region_bed reference/Tair10_genome.bed \
--met_bed ../input/Step8_Input/porec_rep2/forstep08/Rep2_fast5s.C.call_mods.CG.frequency.bed \
--prefix Rep2_fast5s.C.call_mods.CG \
--binsize 100000 \
--outdir ../output
