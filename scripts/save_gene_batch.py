def save_gene_batch(data_df, map_sr):
    
  sfg_arr = two_step(data_df.expr, data_df.ctrl, robust=True)
  save_gene(sfg_arr, map_sr, '../data/sfg_two.txt')

  sfg_arr = pca_based(data_df.expr, data_df.ctrl, robust=True)
  save_gene(sfg_arr, map_sr, '../data/sfg_pca.txt')

  deg_arr = deg(data_df.expr, data_df.ctrl, fc_cutoff=0.5)
  save_gene(deg_arr, map_sr, '../data/deg.txt')

if __name__ == '__main__':
  save_gene_batch(data_df, map_sr)
