# 说明：功能为将blast6out格式的结果每一个ASV可以对应上的所有细菌基因组的ID结果，存到了result文件夹中
# 然后，将利用迭代集合，将每个ASV唯独可以匹配上的细菌基因的ID找寻出来(其他ASV不可能共有的)。输出来的结果，最后通过人为实现每个ASV唯一对应细菌基因组ID。
# 如果输出的结果刚好每个ASV都能匹配到一个唯一的基因组ID，就很完美。但事实是有部分ASV无法唯一匹配上细菌基因组，但允许不同ASV可以对应同一个基因组。
# 因此，这个代码其实可以不用，直接vsearch blast6out结果直接取第一个匹配结果即可。也就是此脚本的第一部分代码的结果。
# 但这个脚本得出来的结果能最大限度地保证一个ASV对应一个唯一的基因组ID。
import os, argparse
import pandas as pd

parser = argparse.ArgumentParser(description="Matching ASVs to unique genomes")
parser.add_argument('-i', '--inputFilePath', metavar='blast6Format', required=True, help='Input blast6out format file path')
parser.add_argument('-o1', '--outputFilePath', metavar='asvToGenome', required=True, help='Output asv to genome id file path')
parser.add_argument('-o2', '--outputFolderPath', metavar='outputFolder', required=True, help='Output folder path')
args = parser.parse_args()

originaDataFrame = pd.read_csv(args.inputFilePath, encoding='utf-8', sep='\t', header=None)
originaDataFrameGroupby = originaDataFrame.groupby(by=0, group_keys=False)
originaDataFrame1 = originaDataFrameGroupby.apply(lambda x: x.sort_values(by=2, ascending=False))
# originaDataFrame1.to_csv('originaDataFrame1_Intermediate_file_viewing.xls', sep='\t')
originaDataFrame2 = originaDataFrame1.reset_index(drop=True)
# originaDataFrame2.to_csv('originaDataFrame2_Intermediate_file_viewing.xls', sep='\t')
originaDataFrame3 = originaDataFrame2[originaDataFrame2[2] >= 99.6]
# originaDataFrame3.to_csv('originaDataFrame3_Intermediate_file_viewing.xls', sep='\t')
originaSeriesGroupby = originaDataFrame3.groupby(by=0, group_keys=False)

resultFolder = args.outputFolderPath
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    else:
        pass
mkdir(resultFolder)
dirPath = os.path.abspath(resultFolder)

for key, valueDf in originaSeriesGroupby:
    outFileNamePath = dirPath+'/'+key + '.txt'
    outFile = open(outFileNamePath, 'w', encoding='utf-8')
    valueDf = valueDf.reset_index(drop=True)
    valueDf = valueDf.drop_duplicates(subset=[1])
    matchGenomeIDList = valueDf[1].values.tolist()
    outFile.write('\n'.join(matchGenomeIDList)+'\n')
    outFile.close()

dirList1 = os.listdir(resultFolder)
dirPath1 = os.path.abspath(resultFolder)

def adjustIfSingle(filePath1):
    dataFrame = pd.read_csv(filePath1, encoding='utf-8', sep='\n', header=None)
    genomeIdList = dataFrame[0].values.tolist()
    genomeIdSet = set(genomeIdList)

    return genomeIdSet


allGenomeIdDict = {}
for fileName1 in dirList1:
    filePath1 = os.path.join(dirPath1,fileName1)
    adjustIfSingle(filePath1)
    genomeIdSet = adjustIfSingle(filePath1)
    allGenomeIdDict[fileName1.rsplit('.', 1)[0]] = genomeIdSet

n = -1
allGenomeIdSetList = list(allGenomeIdDict.values())
allAsvIdList = list(allGenomeIdDict.keys())
j = -1
for i in range(len(allGenomeIdSetList)):
    xSet = allGenomeIdSetList[i]
    while i + 1 < len(allGenomeIdSetList):
        xSet = xSet - allGenomeIdSetList[i + 1]
        i += 1

    j += 1
    allGenomeIdSetList[j] = xSet

allGenomeIdUniqueDict = {}
for m in range(len(allGenomeIdSetList)):
    allGenomeIdUniqueDict[allAsvIdList[m]] = allGenomeIdSetList[m]

outFile2 = open(args.outputFilePath, 'w', encoding='utf-8')
for key, value in allGenomeIdUniqueDict.items():
    outFile2.write(key + '\t' + ('\t').join(value)+ '\n')

# Created by Huilong Chen. July 19, 2023!
# Revised by Huilong Chen. November 26, 2023! object-oriented programming.
