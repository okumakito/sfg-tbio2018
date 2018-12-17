
def load_GSE77578():

  file_name = '../data/GSE77578_series_matrix.txt'
  df = pd.read_csv(file_name, sep='\t', header=[29,65], index_col=0)
  df.drop('!series_matrix_table_end', inplace=True) # => 22697 x 56

  # take two conditions & rename columns
  sr = df.columns.get_level_values(0)
  sr = sr.str.split('_rep').str[0]
  sr = sr.str.replace('hippocampus_pilocarpine_vehicle', 'ctrl')
  sr = sr.str.replace('hippocampus_pilocarpine_PLX3397_3_mg/kg', 'expr')
  df.columns = sr
  df = df.loc[:, ['ctrl','expr']]  # => 22697 x 35 (17 & 18)

  # NOTE: global normalization has been already performed.
  #sns.boxplot(data=df.values, showfliers=False)
  #print(data_df.describe())
  
  return df

def load_GPL6885():
  return pd.read_csv('../data/GPL6885-11608.txt', sep='\t', comment='#',
                     usecols=['ID','ILMN_Gene'], index_col=0, squeeze=True)

if __name__ == '__main__':
  data_df = load_GSE77578()
  map_sr = load_GPL6885()
