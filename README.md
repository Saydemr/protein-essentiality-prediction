# EPPuGNN

This is the repository of a senior project titled "**E**ssential **P**rotein **P**rediction **u**sing **G**raph **N**eural **N**etworks". Project investigates state-of-the-art Graph Neural Network models that fits to essentiality prediction. GNN models utilized are node2vec, GraphSAGE and BLEND. Other computational, topological etc. methods are provided to see the progress clearer. XGBoost is used as the classification algorithm. Use of several biological information sources to enhance the prediction is also analyzed. Relevant materials including code, data, documents etc. are all published to this repository.

## How To

### Pre-requisities
- Python >= 3.8 with Pip

### Clone the repository
```
git clone --depth 1 https://github.com/Saydemr/EPPuGNN.git
```
### Call update.py to download requirements and latest biological data
```
python update.py
```
If you see anything that points to an error, you can download the missing files from [here](https://drive.google.com/drive/folders/1iCOUWxvvAYtPaAUbcvRW-95dP2I64tOd). Downloaded files must be placed under `./data` directory.

### Compile data needed for each GNN
```
cd ./data && python networkx_parser.py --organism sc
```
Outputs will be placed under respective directories of the GNNs.

### Run GNNs to get results.
For now refer, to the GitHub pages of the each GNN. This part will be updated after the automated pipeline is considered as ready.


## Project Information
- Supervisor: [Dr. Emre Sefer](http://www.emresefer.com)
- Institution: [Ozyegin University](https://www.ozyegin.edu.tr/en)

### Members
- [Burcu Arslan](https://github.com/burcula)
- [Abdullah Saydemir](https://github.com/Saydemr)

### Special Thanks
- We would like to thank [Esad Simitcioglu](https://github.com/EsadSimitcioglu), [OzU AI Labs](https://ailabs.ozyegin.edu.tr/) and [Dr. Reyhan Aydoğan](https://www.ozyegin.edu.tr/tr/akademik-kadro/reyhanaydogan) for providing on-demand hardware equipment.
