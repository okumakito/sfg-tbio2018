# sfg-tbio2018

This repository provides source codes used in the following work.

* Makito Oku: "Two novel methods for extracting synchronously fluctuated genes", IPSJ Transactions on Bioinformatics, 12:9-16 (2019). https://doi.org/10.2197/ipsjtbio.12.9

## Requirements

The source codes are written in Python 3. In addition, NumPy, SciPy, pandas, Matplotlib, scikit-learn, and seaborn packages are required. All of them are included in Anaconda.

Gene expression data GSE77578 and its platform data GPL6885 are analyzed. Since their data sizes are large, they are excluded in this repository. Therefore, in order to run the source codes locally, please download the two data sets from [Gene Expression omnibus (GEO)](https://www.ncbi.nlm.nih.gov/geo/) database and put them into the *data* directory.
