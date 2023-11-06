#%config InlineBackend.figure_format = 'retina'
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager as font_manager
import matplotlib as mpl
import matplotlib.patches as mp
import seaborn as sns
import pandas as pd
import click
from hurry.filesize import size,si

@click.command()
@click.option('--cg_bedg',type = str,help = 'CG_bedgraph')
@click.option('--chg_bedg',type = str,help = 'CHG_bedgraph')
@click.option('--chh_bedg',type = str,help = 'CHH_bedgraph')
@click.option('--region_bed',type = str,help = 'the chromosome coordinations in bed')
@click.option('--chrom', type = str, help = 'the chromosome to draw')
@click.option('--outdir', type = str, help = 'The output folder')
def plot_met_chr(cg_bedg,chg_bedg,chh_bedg,region_bed,chrom,outdir):
    CG_table = pd.read_table(cg_bedg,names=['chrom','binstart','binend','met_level_final'],
                             header=None,
                             converters={'chrom':str,'binstart':int,'binend':int})
    CHG_table = pd.read_table(chg_bedg,names=['chrom','binstart','binend','met_level_final'],
                             header=None,
                             converters={'chrom':str,'binstart':int,'binend':int})
    CHH_table = pd.read_table(chh_bedg,names=['chrom','binstart','binend','met_level_final'],
                             header=None,
                             converters={'chrom':str,'binstart':int,'binend':int})

    region_df = pd.read_table(region_bed,header=None,names=['chrom','chr_start','chr_end'],
                                converters={'chrom':str,'chr_start':int,'chr_end':int},
                                index_col = 0)

    region_df.index = region_df.index.astype('str')
    chrom_size = region_df.loc[chrom,'chr_end'] - region_df.loc[chrom,'chr_start']


    font_dirs = ['/public/home/mowp/test/fonts/']
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)

    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['font.size'] = 30
    plt.rcParams['svg.fonttype'] = 'none'
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15,8), sharey=True)

    color_list = ['#262180','#4C7C5D','#632523']

    n = 0
    for i in [CG_table,CHG_table,CHH_table]:
        df = i.query('chrom == @chrom')
        if df['met_level_final'].isnull().sum() > 0:
            sns.lineplot(data=df,x='binstart',y='met_level_final',
            hue=df["met_level_final"].isna().cumsum(),
            palette=[color_list[n]]*sum(df["met_level_final"].isna()),
            lw=4,ax=ax)
        else:
            sns.lineplot(data=df,x='binstart',y='met_level_final',color=color_list[n],lw=4,ax=ax)

        ax.set_xticks([0, chrom_size])
        ax.set_xticklabels([0, size(chrom_size, system=si)])
        ax.title.set_text(f'Chr{chrom}')
        sns.despine(ax=ax)
        n += 1 

    from matplotlib.lines import Line2D
    custom_lines = [Line2D([0], [0], color='#262180', lw=4),
                    Line2D([0], [0], color='#4C7C5D', lw=4),
                    Line2D([0], [0], color='#632523', lw=4)]

    ax.legend(custom_lines, ['CG','CHG','CHH'],loc='upper right')
    #ax[1].spines['right'].set_color('none')
    #ax[1].spines['bottom'].set_color('none')
    #ax[1].spines['left'].set_color('none')
    #ax[1].spines['top'].set_color('none')
    #ax[1].set_xticks([])
    #ax[1].set_yticks([])


    plt.ylim(0, 1)
    plt.yticks([0, 1])
    ax.set_ylabel('Methylation Level')

    plt.savefig(f'{outdir}/Chr{chrom}_methylation_distribution.png',format='png',dpi=300,bbox_inches='tight')

if __name__ == '__main__':
    plot_met_chr()
