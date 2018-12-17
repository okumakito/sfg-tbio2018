def loop_jac(data_df):

  cond_list = [(deg, 'DEG', dict(fc_cutoff=0.5)),
               (two_step, 'Two-step', dict(robust=True)),
               (two_step, 'Two-step (non-robust)', dict(robust=False)),
               (pca_based, 'PCA-based', dict(robust=True)),
               (pca_based, 'PCA-based (non-robust)', dict(robust=False))]
   
  result_list = []
  for func, method, kws in cond_list:
    gene_arr1 = func(data_df.expr, data_df.ctrl, **kws)
    idx_arr = np.arange(data_df.expr.shape[1])
    for n_remove in range(1,11):
      print(method, n_remove)
      jac_list = []
      for i in range(len(idx_arr)):
        # remove one sample
        expr_df1 = data_df.expr.iloc[:, np.delete(idx_arr, i)]
        gene_arr2 = func(expr_df1, data_df.ctrl, **kws)
        jac_list.append(jaccard(gene_arr1, gene_arr2))
      
      min_idx = np.argmin(jac_list)
      idx_arr = np.delete(idx_arr, min_idx)
      result_list.append(dict(n_remove=n_remove,
                              jaccard=jac_list[min_idx],
                              method=method))

  return pd.DataFrame(result_list)
    

if __name__ == '__main__':
  df_jac = loop_jac(data_df)

  
