def plot_fpr(df_f1, metric):  # metric: 'f1', 'p', or 'r'

  with sns.plotting_context('talk'):

    fig, ax = plt.subplots()
    hue_order = ['Two-step','PCA-based']
    hue_order2 = ['Two-step (non-robust)','PCA-based (non-robust)']
    label_dict = dict(f1='F1 score', p='Precision', r='Recall')

    sns.pointplot(data=df_f1, x='n_sample', y=metric, hue='method',
                  dodge=0.1, hue_order=hue_order, linestyles='-')
    sns.pointplot(data=df_f1, x='n_sample', y=metric, hue='method',
                  dodge=0.1, hue_order=hue_order2, linestyles='--',
                  markers='x')

    ax.legend(frameon=False, loc='lower right')
    ax.set_xlabel('Number of samples')
    ax.set_ylabel(label_dict[metric])
    ax.set_ylim((-0.05, 1.05))

    fig.tight_layout()
    #fig.show()

    
if __name__ == '__main__':
  plot_fpr(df_fpr, 'f1')
  plot_fpr(df_fpr, 'p')
  plot_fpr(df_fpr, 'r')
