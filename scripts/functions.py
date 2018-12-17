import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from scipy import stats
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.decomposition import PCA

# utils --------------------------------------------------------------------

def mad(df): # median absolute deviation
  return df.subtract(df.median(axis=1), axis=0).abs().median(axis=1)

def score_from_index(func, idx_seq1, idx_seq2, n):
  x1 = np.zeros(n)
  x2 = np.zeros(n)
  x1[idx_seq1] = 1
  x2[idx_seq2] = 1
  return func(x1, x2)

def score_sfg(sfg_arr, func):
  return score_from_index(func, np.arange(500), sfg_arr, 10000)

def jaccard(idx_seq1, idx_seq2):
  return len(np.intersect1d(idx_seq1, idx_seq2)) / \
         len(np.union1d(idx_seq1, idx_seq2))

def generate_data(n_sample, scale=5, n_gene=10000, n_pos=500):
  df_expr = pd.DataFrame(np.random.randn(n_gene, n_sample))
  df_ctrl = pd.DataFrame(np.random.randn(n_gene, n_sample))
  common_fluc = np.sqrt(scale**2 - 1) * np.random.randn(n_sample)
  df_expr[:n_pos] += common_fluc
  return df_expr, df_ctrl

def deg(df_expr, df_ctrl, fc_cutoff=1.0):
  # differentially expressed genes
  diff_sr = df_expr.mean(axis=1) - df_ctrl.mean(axis=1)
  return df_expr.index[diff_sr.abs() > fc_cutoff]

def save_gene(gene_arr, map_sr, file_name='gene_list.txt'):
  pd.Series(map_sr.loc[gene_arr].dropna().sort_values().unique()).\
    to_csv(file_name, index=False)
  
def calculate_q(p_seq):
  p_arr          = np.asarray(p_seq)
  n_tests        = len(p_arr)
  sort_index_arr = np.argsort(p_arr)
  p_sorted_arr   = p_arr[sort_index_arr]
  q_arr          = p_sorted_arr * n_tests / (np.arange(n_tests) + 1)
  q_min          = q_arr[-1]
  q_list         = [q_min]
  for q in q_arr[-2::-1]:
    if q < q_min:
      q_min = q
    q_list.append(q_min)
  q_arr = np.array(q_list)[::-1]
  q_arr[sort_index_arr] = q_arr.copy()
  return q_arr

# proposed method 1 --------------------------------------------------------

def two_step(df_expr, df_ctrl, fc_cutoff=2, corr_cutoff=0.75,
             cluster_cutoff=0.5, robust=True):

  # step 1: deviation filtering
  if robust:
    df_sub = df_expr[mad(df_expr) > fc_cutoff * mad(df_ctrl)]
  else:
    df_sub = df_expr[df_expr.std(axis=1) > fc_cutoff * df_ctrl.std(axis=1)]
  
  # step 2: clustering
  if robust:
    # Spearman's correlation
    df_sub = df_sub.T.rank().T
  linkage_arr = linkage(df_sub, method='average', metric='correlation')
  label_arr = fcluster(linkage_arr, 1-corr_cutoff, criterion='distance')
  freq_sr = pd.Series(label_arr).value_counts()
  clust_idx = freq_sr.index[freq_sr > cluster_cutoff * freq_sr.iat[0]]
  return df_sub.index[np.isin(label_arr, clust_idx)]

# proposed method 2 --------------------------------------------------------

def pca_based_sub(df, outlier_cutoff=1.5, robust=True):

  # outlier detection
  df_trans = df.T.copy()
  if robust:
    q1_sr= df.quantile(0.25, axis=1)
    q3_sr= df.quantile(0.75, axis=1)
    iqr_sr = q3_sr - q1_sr # interquartile range
    df_trans[df_trans < (q1_sr - outlier_cutoff * iqr_sr)] = None
    df_trans[df_trans > (q3_sr + outlier_cutoff * iqr_sr)] = None
  df_trans -= df_trans.mean()
  df_trans.fillna(0, inplace=True)

  # pca
  model = PCA(n_components=1)
  model.fit(df_trans)
  return np.abs(model.components_[0]) * np.sqrt(model.explained_variance_[0])
  
def pca_based(df_expr, df_ctrl, outlier_cutoff=1.5, sigma_cutoff=3,
              robust=True):
  c_expr_arr = pca_based_sub(df_expr, outlier_cutoff, robust)
  c_ctrl_arr = pca_based_sub(df_ctrl, outlier_cutoff, robust)
  diff_arr = c_expr_arr - c_ctrl_arr
  return df_expr.index[diff_arr > diff_arr.mean() +
                       sigma_cutoff * diff_arr.std(ddof=1)]


