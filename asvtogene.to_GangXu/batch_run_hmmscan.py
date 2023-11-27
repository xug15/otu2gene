import os, subprocess, signal, argparse

parser = argparse.ArgumentParser(description="Batch annotation of genotypes via HMMER")
parser.add_argument('-i', '--inputFolderPath', metavar='targetProteome', required=True, help='Input Path to the folder holding the target bacterial proteomes')
parser.add_argument('-o', '--outputFolderPath', metavar='outputFolder', required=True, help='Output folder path')
args = parser.parse_args()

# multifasta
# folder1 = r'genome_extract_result'
folder1 = args.inputFolderPath
dirList1 = os.listdir(folder1)
# print(dirList1)
dirPath1 = os.path.abspath(folder1)
# print(dirPath1)

# blast_result_dir
# folder2 = r'hmmscanResult'
folder2 = args.outputFolderPath
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    else:
        pass

mkdir(folder2)
dirPath2 = os.path.abspath(folder2)

for fileName1 in dirList1:
    filePath1 = os.path.join(dirPath1, fileName1)
    hmmscanResultPathName = dirPath2 + '/' + fileName1.rsplit('_', 1)[0] + '_hmmscan.tbl'
    command = "hmmscan -o out.txt --tblout {} --noali -T 10 /public/home/2022122/chenhuilong/ph_preference/pfam_annotation/Pfam-A.hmm {}".format(str(hmmscanResultPathName), str(filePath1))
    process = subprocess.Popen(command, universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    stdoutput, erroutput = process.communicate()

    print("{}, process.returncode: {}".format(hmmscanResultPathName, process.returncode))
    if process.returncode:
        print(hmmscanResultPathName, 'errOutput: ', erroutput.strip('\n'), sep=', ', end='***\n')
        print(hmmscanResultPathName, 'stdOutput: ', stdoutput.strip('\n'), sep=', ', end='***\n')
        if process.returncode < 0:
            print('The process calling the hmmscan program was killed by the system!')
        # print('chenhuilong1\n')
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except BaseException as e:
            if str(e) != "[Errno 3] No such process":
                print(e)
        continue
    else:
        pass

# Created by Huilong Chen, August 7, 2023.
# Revised by Huilong Chen. November 26, 2023! object-oriented programming.
