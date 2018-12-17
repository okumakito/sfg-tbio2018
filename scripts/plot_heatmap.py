def plot_heatmap(data_df, func=two_step, robust=True):

  sfg_arr = func(data_df.expr, data_df.ctrl, robust=robust)
  df_trans = data_df.loc[sfg_arr].T
  df_trans = (df_trans - df_trans.mean()) / df_trans.std()
  df = df_trans.T

  linkage_arr = linkage(df_trans.rank().T, method='average',
                        metric='correlation')
  sort_list = dendrogram(linkage_arr, no_plot=True)['leaves']

  with sns.plotting_context('talk'):
    fig, ax = plt.subplots(figsize=(6,4))
    sns.heatmap(df.iloc[sort_list],
                cmap        = plt.cm.RdBu_r,
                cbar        = True,
                ax          = ax,
                cbar_kws    = dict(orientation='horizontal',
                                   shrink=0.5, pad=0.1))

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel(' '*5 + 'Control group' + ' '*15 + 'Experimental group')
    ax.set_ylabel('Genes')
    ax.axvline(x=17, lw=5, c='black')
    fig.tight_layout()
    #fig.show()

    
if __name__ == '__main__':
  plot_heatmap(data_df, two_step, robust=True)
  plot_heatmap(data_df, two_step, robust=False)
  plot_heatmap(data_df, pca_based, robust=True)
  plot_heatmap(data_df, pca_based, robust=False)
