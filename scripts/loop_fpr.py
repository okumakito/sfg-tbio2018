def loop_fpr(n_repeat):

  cond_list = [(two_step, 'Two-step', dict(robust=True)),
               (two_step, 'Two-step (non-robust)', dict(robust=False)),
               (pca_based, 'PCA-based', dict(robust=True)),
               (pca_based, 'PCA-based (non-robust)', dict(robust=False))]
  
  np.random.seed(0)
  result_list = []
  for n_sample in [3,4,5,6,7,8,9,10,15,20,25,30]:
    print(n_sample)
    for func, method, kws in cond_list:
      for _ in range(n_repeat):
        X, Y = generate_data(n_sample)
        sfg_arr = func(X, Y, **kws)
        result_list.append(dict(n_sample=n_sample,
                                method=method,
                                f1=score_sfg(sfg_arr, f1_score),
                                p=score_sfg(sfg_arr, precision_score),
                                r=score_sfg(sfg_arr, recall_score)))

  return pd.DataFrame(result_list)
    
    
if __name__ == '__main__':
  df_fpr = loop_fpr(100)
