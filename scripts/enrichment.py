def enrichment(file_name, fdr=0.05):
  df = pd.read_csv(file_name, sep='\t',
                   usecols=['Term','Count','List Total',
                            'Pop Hits','Pop Total'])
  n_test = df.shape[0]
  print('number of tests: ' + str(n_test))
  p_list = []
  for i, (term, x, n1, n2, N) in df.iterrows():
    # Fisher's exact test
    p_list.append(stats.hypergeom.sf(x-1, N, n1, n2))
  q_arr = calculate_q(p_list)
  df['p-value'] = p_list
  df['q-value'] = q_arr
  df = df[df['q-value'] <= fdr]
  df['Term'] = df['Term'].str.split('~').str[1]
  df.sort_values(['Count','p-value','Term'], inplace=True,
                 ascending=[False,True,True])

  df['p-value'] = df['p-value'].map('{:.1e}'.format)
  df['q-value'] = df['q-value'].map('{:.1e}'.format)
  print(df.head(10), end='\n\n')

    
if __name__ == '__main__':
  enrichment('../data/sfg_two_go.txt', fdr=0.2)
  enrichment('../data/sfg_pca_go.txt', fdr=0.05)
  enrichment('../data/deg_go.txt', fdr=0.05)
