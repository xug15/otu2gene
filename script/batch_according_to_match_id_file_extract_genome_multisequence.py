import os, shutil, argparse
import pandas as pd

parser = argparse.ArgumentParser(description="Batch extraction of target bacterial proteome")
parser.add_argument('-i', '--inputFilePath', metavar='asvToGenome', required=True, help='Input asv to genome id file path')
parser.add_argument('-d', '--inputDatabaseFolderPath', metavar='proteomeDatabase', required=True, help='Path to the folder holding the bacterial proteomes')
parser.add_argument('-o', '--outputFolderPath', metavar='outputFolder', required=True, help='Output folder path')
args = parser.parse_args()

# folder1 = r'/public/home/2022122/chenhuilong/ph_preference/data/protein_faa_reps/bacteria_processed'
folder1 = args.inputDatabaseFolderPath
dirList1 = os.listdir(folder1)
dirPath1 = os.path.abspath(folder1)

resultFolder = args.outputFolderPath
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    else:
        pass
mkdir(resultFolder)
dirPath2 = os.path.abspath(resultFolder)

def myCopyFile(srcfile, dstpath):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)
        shutil.copy(srcfile, dstpath + fname)

idMatchDataFrame = pd.read_csv(args.inputFilePath, sep = '\t', encoding = 'utf-8', header=None)
idMatchDataFrame2 = idMatchDataFrame.drop_duplicates(subset=[1])
uniqueGenomeIdList = idMatchDataFrame2[1].values.tolist()

for fileName1 in dirList1:
    filePath1 = os.path.join(dirPath1, fileName1)
    if fileName1.rsplit('_', 1)[0] in uniqueGenomeIdList:
        myCopyFile(filePath1, dirPath2+'/')

# Created by Huilong Chen, July 20, 2023!
# Revised by Huilong Chen. November 26, 2023! object-oriented programming.
