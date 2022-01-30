import os, fnmatch
import requests
import subprocess
import sys
import zipfile



# Install requirements
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])


# Update BIOGrid data files
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
        return version_number - 1

# Get the current version
files = fnmatch.filter(os.listdir('./data'), 'BIOGRID-ORGANISM-4.4.*.tab3.zip')
if len(files) == 0:
    version_number = 204
    FLAG = False
else:
    version_number = int(files[0].split('.')[-3])

# Check the recent version
most_recent = most_recent_available(version_number)

# If the next version is available, download it
if most_recent > version_number:
    
    # Download the file
    url = "https://downloads.thebiogrid.org/Download/BioGRID/Release-Archive/BIOGRID-4.4." + str(most_recent) + "/BIOGRID-ORGANISM-4.4." + str(most_recent) + ".tab3.zip"
    r = requests.get(url, stream=True)
    with open('./data/BIOGRID-ORGANISM-4.4.{}.tab3.zip'.format(most_recent), 'wb') as f:
        f.write(r.content)
    
    # Unzip the file
    zf = zipfile.ZipFile('./data/BIOGRID-ORGANISM-4.4.{}.tab3.zip'.format(most_recent), 'r')
    filelist = [x for x in zf.filelist if 'Homo_sapiens' in x.filename or 'Mus_musculus' in x.filename or 'Saccharomyces_cerevisiae' in x.filename]
    for file in filelist:
        zf.extract(file, './data')

    # Remove the old files if exist
    if FLAG:
        os.remove('./data/BIOGRID-ORGANISM-4.4.{}.tab3.zip'.format(version_number))
        os.remove('./data/BIOGRID-ORGANISM-Homo_sapiens-4.4.{}.tab3.txt'.format(version_number))
        os.remove('./data/BIOGRID-ORGANISM-Saccharomyces_cerevisiae*-4.4.{}.tab3.txt'.format(version_number))
        os.remove('./data/BIOGRID-ORGANISM-Mus_musculus-4.4.{}.tab3.txt'.format(version_number))    
else:
    print("Most recent version")

