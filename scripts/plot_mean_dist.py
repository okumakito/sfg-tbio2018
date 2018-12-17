def plot_mean_dist(data_df):

  with sns.plotting_context('talk'):

    fig, ax = plt.subplots()
    
    mean_sr = data_df.mean(axis=1)
    ratio_sr = mad(data_df.expr) / mad(data_df.ctrl)
    diff_arr = pca_based_sub(data_df.expr) - pca_based_sub(data_df.ctrl)
    diff_sr = pd.Series(diff_arr, index=data_df.index)

    kws = dict(hist=False, kde_kws={'shade':True})
    sns.distplot(mean_sr, label='All genes', **kws)
    sns.distplot(mean_sr[ratio_sr > ratio_sr.quantile(0.9)],
                 label='Two-step, top 10 % MAD ratio', **kws)
    sns.distplot(mean_sr[diff_sr > diff_sr.quantile(0.9)],
                 label='PCA-based, top 10 % contribution difference', **kws)

    ax.legend(frameon=False)
    ax.set_xlim((mean_sr.min(), mean_sr.max()))
    ax.set_xlabel('Average gene expression')
    ax.set_ylabel('Probability')

    fig.tight_layout()
    #fig.show()

    
if __name__ == '__main__':
  plot_mean_dist(data_df)
