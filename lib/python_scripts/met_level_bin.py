import pandas as pd
import click 
import numpy as np

@click.command()
@click.option('--region_bed',type=str,help = 'region bed')
@click.option('--met_bed',type=str,help = 'file with single cytosine met level')
@click.option('--prefix',type=str,help='prefix')
@click.option('--binsize',type=int,help='binsize')
@click.option('--outdir', type=str, help='outdir')
def level_size(region_bed,met_bed,prefix,binsize,outdir):
    region_df = pd.read_table(region_bed,header=None,names=['chrom','chr_start','chr_end'],
                            converters={'chrom':str,'chr_start':int,'chr_end':int},
                            index_col = 0)
    
    region_df.index = region_df.index.astype('str')

    met_df = pd.read_table(met_bed,header=None, 
                       usecols=[0,1,2,5,9,10],
                       names=['chrom','start','end','strand','coverage','met_percentage'],
                       converters={'chrom':str,'start':int,'end':int,'strand':str,'coverage':int,'met_percentage':float})

    #Keep the valid sites that have more than 4 reads mapped
    met_df_valid = met_df.query('coverage >= 4')

    #divide the sites into different bins
    met_df_interval = pd.DataFrame([])
    for i in region_df.itertuples():
        region_chr,region_start,region_end = i
        query_text = '(chrom == @region_chr) and (start > @region_start) and (end <= @region_end)'
        met_df_tmp = met_df_valid.query(query_text)
        df_cut = pd.cut(met_df_tmp['start'],bins=np.arange(region_start,region_end+binsize,binsize),right=False,precision=0)
        met_df_tmp.loc[:,'interval'] = df_cut
        #keep all bins in the region to fill gap for no methylated bins
        region_interval_tmp = pd.DataFrame([])
        region_interval_tmp.loc[:,'interval'] = df_cut.dtype.categories
        region_interval_tmp.loc[:,'chrom'] = region_chr
        met_df_fillgap = pd.merge(met_df_tmp,region_interval_tmp,how='right')
        met_df_fillgap.loc[:,'met_percentage'] = met_df_fillgap['met_percentage'].fillna(0)
        met_df_interval = met_df_interval.append(met_df_fillgap)

    #calculate the weighted methylation level with the valid sites within each bin
    met_df_interval_group = met_df_interval.groupby(
        by=['chrom','interval']).apply(
        lambda df: df.assign(
            met_level = ((df['coverage']*df['met_percentage']/100).sum())/(df['coverage'].sum()) if (df['coverage'].sum() != 0) else 0,size = len(df)))



    #Keep the valid bin methylation level, while write the unvalid bin methylation level as NA
    met_df_bin_filter =  met_df_interval_group.assign(
        met_level_final = lambda df: np.select(
            [df['size'] < 4, df['size']>= 4],
            [np.nan,df['met_level']]
        )
    )

    #transform to bedgraph format
    met_df_bedgraph = met_df_bin_filter.reindex(['chrom','interval','met_level_final'],axis=1).drop_duplicates()

    #spit the bin interval into two columna
    idx = pd.IntervalIndex(met_df_bedgraph['interval'])
    met_df_bedgraph_split_bin = met_df_bedgraph.assign(binstart =idx.left, binend = idx.right)
    met_df_bedgraph_split_bin['binstart'] = met_df_bedgraph_split_bin['binstart'].astype(int)
    met_df_bedgraph_split_bin['binend'] = met_df_bedgraph_split_bin['binend'].astype(int)
    met_df_bedgraph_split_bin.to_csv(f'{outdir}/{prefix}_binsize{binsize}.bedgraph',
                                     columns=['chrom','binstart','binend','met_level_final'],
                                     sep="\t",header=None,index=False,
                                     float_format="%.2f")
if __name__ == '__main__':
    level_size()
