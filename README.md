# EPPuGNN

This is the repository of a senior project titled **E**ssential **P**rotein **P**rediction **u**sing **G**raph **N**eural **N**etworks. Project investigates state-of-the-art Graph Neural Network models that fits to essentiality prediction. GNN models utilized are [node2vec](https://github.com/aditya-grover/node2vec), [GraphSAGE](https://github.com/williamleif/GraphSAGE) and two diffusion based GNNs namely [GRAND](https://github.com/twitter-research/graph-neural-pde) and [BLEND](https://github.com/twitter-research/graph-neural-pde). Other computational, topological etc. methods are provided to see the progress clearer. [XGBoost](https://github.com/dmlc/xgboost) is used as the classification algorithm for unsupervised models. Use of several biological information sources such as gene expressions, go annotations to enhance the prediction is also analyzed. Relevant materials including code, data, documents etc. are all published to this repository.

## How To

### Pre-requisities
- [Conda](https://www.anaconda.com/products/distribution) Latest
- [Python](https://www.python.org/downloads/) v3.9
- [CUDA](https://developer.nvidia.com/cuda-11.3.0-download-archive) v11.3


### Clone the repository
```
git clone --depth 1 https://github.com/Saydemr/EPPuGNN.git
```

### Create Environment
```
conda env create -f environment.yml
conda activate eppugnn
```

### Download requirements and latest biological data
```
python update.py
```
If you see anything that points to an error, you can download the missing files from [here](https://drive.google.com/drive/folders/1iCOUWxvvAYtPaAUbcvRW-95dP2I64tOd). Downloaded files must be placed under `./data` directory before running the next commands.

Biological data are obtained from [BioGRID](https://downloads.thebiogrid.org/BioGRID), [COMPARTMENTS](https://compartments.jensenlab.org/Downloads), and [NHI GEO](https://www.ncbi.nlm.nih.gov/geo/) databases. Links to obtain files can be found inside the [script](update.py).

### Compile data needed for each GNN

Preprocessor takes organism name as an argument. It compiles necessary information for the given organism and saves it under `./data` directory. If you want to create data for all organisms, you can run the following command.
```
cd ./data
python compose_data.py --organism all
```

If you want to create data for a specific organism, you can run the following command.
```
cd ./data
python compose_data.py --organism sc
```

Outputs to be used in each GNN will be placed under respective directories.

### Run GNNs to get results.
For now, refer to the GitHub pages of the each GNN. This part will be updated after the automated pipeline is considered ready.
We forked said GNNs to integrate some necessary features missing in the original repositories.
<!-- You can find our forks from [here](https://github.com/Saydemr/GraphSAGE) and [here](https://github.com/Saydemr/pde). -->


## Project Information
- Supervisor: [Dr. Emre Sefer](http://www.emresefer.com)
- Institution: [Ozyegin University](https://www.ozyegin.edu.tr/en)

### Members
- [Burcu Arslan](https://github.com/burcula)
- [Abdullah Saydemir](https://github.com/Saydemr)

### Special Thanks
- We would like to thank [Esad Simitcioglu](https://github.com/EsadSimitcioglu), [OzU AI Labs](https://ailabs.ozyegin.edu.tr/) and [Dr. Reyhan Aydoğan](https://www.ozyegin.edu.tr/en/faculty/reyhanaydogan) for providing on-demand hardware equipment.
