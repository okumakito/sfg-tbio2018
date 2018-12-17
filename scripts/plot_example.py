def plot_example(idx): # 0: deg, 1: sfg

  n_sample = 6
  n_gene = 2
  np.random.seed(idx)  

  df = pd.DataFrame()
  df['sample'] = list(range(1, 2*n_sample+1)) * n_gene
  df['value'] = 0.1*np.random.randn(2*n_sample*n_gene)
  x_arr = [1.2 *np.ones(n_sample),
           1.0*np.random.randn(n_sample)][idx]
    
  class_list = []
  for i in range(1,n_gene+1):
    df.iloc[(2*i-1)*n_sample:(2*i)*n_sample,1] += x_arr
    class_list += ['gene ' + str(i)] * n_sample*2
  df['class'] = class_list
    
  with sns.plotting_context('talk'):

    fig, ax = plt.subplots(figsize=(6,4))

    sns.pointplot(data=df, x='sample', y='value', hue='class', ax=ax,
                  join=False, legend=False, dodge=True)

    leg = ax.legend(loc='upper left')
    leg.get_frame().set_linewidth(3)
    ax.set_xlabel('Samples')
    ax.set_ylabel('Normalized gene expression')
    ax.axvline(x=n_sample-0.5, c='0.2', ls='--')
    ax.set_ylim((-2,2))
    ax.text(0.5*n_sample-0.5, -1.8, 'Control', ha='center', va='center')
    ax.text(1.5*n_sample-0.5, -1.8, 'Experimental', ha='center', va='center')
    
    fig.tight_layout()
    #fig.show()

    
if __name__ == '__main__':
  plot_example(0)
  plot_example(1)
