from genericpath import isfile
import subprocess
import sys

# Install requirements
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

import gzip
import shutil
import requests
import fnmatch
import os
from zipfile import ZipFile

# Update BioGRID data files
BASE_URL_TEST = "https://downloads.thebiogrid.org/File/BioGRID/Release-Archive/BIOGRID-4.4.VERSION/BIOGRID-ORGANISM-4.4.VERSION.tab3.zip"
FLAG = True


def most_recent_available(version_number):
    """
    Check if next version is available
    """
    r = requests.get(BASE_URL_TEST.replace("VERSION", str(version_number)))
    if r.status_code == 200:
        return most_recent_available(version_number + 1)
    else:
        return 211


# Get the current version
files = fnmatch.filter(os.listdir('./data'), 'BIOGRID-ORGANISM-4.4.*.tab3.zip')
if len(files) == 0:
    version_number = 206
    FLAG = False
else:
    version_number = int(files[0].split('.')[-3])

# Check the recent version
most_recent = most_recent_available(version_number)

# If the next version is available, download it
if most_recent == 211:
    
    # Remove the old files if exist
    print("Downloading the newest BioGRID version")
    if FLAG:
        files = fnmatch.filter(os.listdir('./data'), 'BIOGRID-ORGANISM-*.tab3*')
        for file in files:
            os.remove('./data/' + file)

    # Download the file
    url = "https://downloads.thebiogrid.org/Download/BioGRID/Release-Archive/BIOGRID-4.4." + \
        str(most_recent) + "/BIOGRID-ORGANISM-4.4." + \
        str(most_recent) + ".tab3.zip"
    r = requests.get(url, stream=True)
    with open('./data/BIOGRID-ORGANISM-4.4.{}.tab3.zip'.format(most_recent), 'wb') as f:
        f.write(r.content)

    # Unzip the file
    zf = ZipFile(
        './data/BIOGRID-ORGANISM-4.4.{}.tab3.zip'.format(most_recent), 'r')
    filelist = [x for x in zf.filelist if 'Homo_sapiens' in x.filename or 'Saccharomyces_cerevisiae' in x.filename]
    for file in filelist:
        zf.extract(file, './data')

else:
    print("Most recent version")

# Download gene expression data
print("Downloading gene expression data")
if not isfile('./data/GSE86354_GTEx_FPKM.txt'):
    expression_human = requests.get('https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE86354&format=file&file=GSE86354_GTEx_FPKM.txt.gz', stream=True)
    with open('./data/GSE86354_GTEx_FPKM.txt.gz', 'wb') as f:
        f.write(expression_human.content)

    with gzip.open('./data/GSE86354_GTEx_FPKM.txt.gz', 'rb') as f_in:
        with open('./data/GSE86354_GTEx_FPKM.txt', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

if not isfile('./data/GPL570-55999.txt'):
    supplementary_hs = requests.get('https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?mode=raw&is_datatable=true&acc=GPL570&id=55999&db=GeoDb_blob143', stream=True)
    with open('./data/GPL570-55999.txt', 'wb') as f:
        f.write(supplementary_hs.content)


if not isfile('./data/GSE3431_series_matrix.txt'):
    expression_sc = requests.get('https://ftp.ncbi.nlm.nih.gov/geo/series/GSE3nnn/GSE3431/matrix/GSE3431_series_matrix.txt.gz', stream=True)
    with open('./data/GSE3431_series_matrix.txt.gz', 'wb') as f:
        f.write(expression_sc.content)

    with gzip.open('./data/GSE3431_series_matrix.txt.gz', 'rb') as f_in:
        with open('./data/GSE3431_series_matrix.txt', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

if not isfile('./data/GPL90-17389.txt'):
    supplementary_sc = requests.get('https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?mode=raw&is_datatable=true&acc=GPL90&id=17389&db=GeoDb_blob144', stream=True)
    with open('./data/GPL90-17389.txt', 'wb') as f:
        f.write(supplementary_sc.content)


# Download the subcellular localization data
print("Downloading subcellular localization data")
if not isfile('./data/human_compartment_knowledge_full.tsv'):
    subcellular_hs = requests.get('https://download.jensenlab.org/human_compartment_knowledge_full.tsv', stream=True)
    with open('./data/human_compartment_knowledge_full.tsv', 'wb') as f:
        f.write(subcellular_hs.content)


if not isfile('./data/yeast_compartment_knowledge_full.tsv'):
    subcellular_sc = requests.get('https://download.jensenlab.org/yeast_compartment_knowledge_full.tsv', stream=True)
    with open('./data/yeast_compartment_knowledge_full.tsv', 'wb') as f:
        f.write(subcellular_sc.content)



if not isfile('./data/degannotation-e.dat'):
    print("Downloading essential genes data")
    essential_genes = requests.get('http://tubic.tju.edu.cn/deg/download/deg-e-15.2.zip', stream=True)
    if essential_genes.status_code == 200:
        with open('./data/deg-e-15.2.zip', 'wb') as f:
            f.write(essential_genes.content)


        with ZipFile('./data/deg-e-15.2.zip', 'r') as z:
            z.extract('degannotation-e.dat', './data/')
    else:
        print("Error downloading essential genes data. Server is down.")

if not isfile('./data/deg_sc.dat'):
    with open ('./data/degannotation-e.dat', 'r') as f:
        with open ('./data/deg_sc.dat', 'w+', encoding='UTF8') as g:
            f.readline()
            for line in f:
                line = line.strip()
                line = line.split('\t')

                if line[7] == 'Saccharomyces cerevisiae':
                    g.write(line[2] + '\n')
            
if not isfile('./data/deg_hs.dat'):
    gene_num_listed = {}
    with open ('./data/degannotation-e.dat', 'r', encoding='UTF8') as f:
        f.readline()
        for line in f:
            line = line.strip()
            line = line.split('\t')
            if line[7] == 'Homo sapiens':
                if line[2] in gene_num_listed:
                    gene_num_listed[line[2]] += 1
                else:
                    gene_num_listed[line[2]] = 1


    print("Preparing Homo Sapiens annotations...")
    with open ('./data/deg_hs.dat', 'w+') as g:
        for key in gene_num_listed:
            if gene_num_listed[key] > 4:
                g.write(key + '\n')
