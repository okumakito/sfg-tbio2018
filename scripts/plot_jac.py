def plot_jac(df_jac):

  with sns.plotting_context('talk'):

    fig, ax = plt.subplots()

    sns.pointplot(data=df_jac, x='n_remove', y='jaccard', hue='method',
                  hue_order=['Two-step', 'PCA-based'],
                  linestyles='-')
    sns.pointplot(data=df_jac, x='n_remove', y='jaccard', hue='method',
                  hue_order=['Two-step (non-robust)',
                             'PCA-based (non-robust)'],
                  linestyles='--', markers='x')

    ax.legend(frameon=False, loc='upper right')
    ax.set_xlabel('Number of removed samples')
    ax.set_ylabel('Jaccard index')

    fig.tight_layout()
    #fig.show()

    
if __name__ == '__main__':
  plot_jac(df_jac)
