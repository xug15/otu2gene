import os, argparse

parser = argparse.ArgumentParser(description="Obtaining full gene presence or absence matrices based on HMMER annotation results")
parser.add_argument('-i', '--inputFilePath', metavar='asvToGenome', required=True, help='Input asv to genome id file path')
parser.add_argument('-m', '--inputFolderPath', metavar='hmmscanResult', required=True, help='Input Path to the folder holding the target HMMER annotation results')
parser.add_argument('-o', '--outputFolderPath', metavar='outputFolder', required=True, help='Output folder path')
args = parser.parse_args()

# multifasta
# folder1 = r'hmmscanResult'
folder1 = args.inputFolderPath
dirList1 = os.listdir(folder1)
dirPath1 = os.path.abspath(folder1)

# result_dir
# folder2 = r'all_gene_presence_absence_table_result'
folder2 = args.outputFolderPath
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    else:
        pass

mkdir(folder2)
dirPath2 = os.path.abspath(folder2)

def getListElementConcatenation(lists):
    resultSet = set()

    for lst in lists:
        resultSet.update(lst)

    resultList = list(resultSet)
    return resultList

allLists = []
for fileName1 in dirList1:
    filePath1 = os.path.join(dirPath1, fileName1)
    hmmGeneList = []
    hmmscanResultFilePathPointer = open(filePath1, 'r', encoding='utf-8')
    for line in hmmscanResultFilePathPointer:
        if line.startswith("#") == False:
            hmmGene = line.strip('\n').split(' ', 1)[0]
            hmmGeneList.append(hmmGene)
    hmmscanResultFilePathPointer.close()
    allLists.append(hmmGeneList)

gene_order = getListElementConcatenation(allLists)
print(len(gene_order))

# gene_order = ["X5.FTHF_cyc.lig", "AAA_25", "AAA_assoc_C", "AcetylCoA_hyd_C", "ASH", "Big_3_5", "CitMHS", "CpsB_CapC",
#               "CpXC", "CsbD", "Cys_rich_CPXG", "Cytidylate_kin2", "CytoC_RC", "DHquinase_I", "Exo_endo_phos",
#               "FAD_binding_7", "Glucodextran_N", "GWxTD_dom", "HipA_2", "HTH_37", "HupF_HypC", "HycI", "HypD",
#               "Ig_GlcNase", "KdpA", "KdpC", "KdpD", "Lactonase", "MCRA", "Met_gamma_lyase", "Methyltransf_4",
#               "MgtE", "MNHE", "MrpF_PhaF", "OprB", "Paired_CXXCH_1", "PDZ_2", "PGI", "PhaG_MnhG_YufB",
#               "Phenol_MetA_deg", "Phosphoesterase", "Polbeta", "PQQ", "Pro.kuma_activ", "SelO", "SNase", "SOUL",
#               "TctA", "TelA", "TFR_dimer", "TPP_enzyme_C", "TrbI", "UvdE", "WXXGXW", "YHS", "zf.CDGSH"]
# print(len(gene_order))

def extractSingleGnenomeIdGenePresenceAbsenceBinarize(hmmscanResultFilePath, gene_order):

    hmmGeneList = []
    for line in hmmscanResultFilePath:
        if line.startswith("#") == False:
            hmmGene = line.strip('\n').split(' ', 1)[0]
            hmmGeneList.append(hmmGene)

    intersectionList = list(set(hmmGeneList) & set(gene_order))
    # print(intersectionList)

    binarizeList = []
    for gene in gene_order:
        if gene in intersectionList:
            binarizeList.append('1')
        else:
            binarizeList.append('0')

    return binarizeList

genomeIdGenePresenceOrAbsenceDict = {}

for fileName1 in dirList1:
    filePath1 = os.path.join(dirPath1, fileName1)
    genomeId = fileName1.rsplit('_', 1)[0]
    hmmscanResultFilePath = open(filePath1, 'r', encoding='utf-8')
    binarizeList = extractSingleGnenomeIdGenePresenceAbsenceBinarize(hmmscanResultFilePath, gene_order)
    genomeIdGenePresenceOrAbsenceDict[genomeId] = binarizeList
    hmmscanResultFilePath.close()

genePresenceAbsenceResultFilePointer = open(dirPath2+'/'+'allGenePresenceAbsenceBinarizeTable.xls', 'w', encoding='utf-8')
genePresenceAbsenceResultFilePointer.write('ASV/OTU'+'\t'+'\t'.join(gene_order)+'\n')

asvVsGenomeFilePointer = open(args.inputFilePath, 'r', encoding='utf-8')
for line in asvVsGenomeFilePointer:
    lineList = line.strip('\n').split('\t')
    asvId = lineList[0]
    genomeId = lineList[1]
    genePresenceAbsenceResultFilePointer.write(asvId+'\t'+'\t'.join(genomeIdGenePresenceOrAbsenceDict[genomeId])+'\n')
asvVsGenomeFilePointer.close()

# Created by Huilong Chen, August 12, 2023!
# Revised by Huilong Chen, November 26, 2023! Modified to the presence or absence matrix of all genes.
# Revised by Huilong Chen. November 26, 2023! object-oriented programming.