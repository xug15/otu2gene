# otu2gene
## 0. Prepare the database.

[https://github.com/fiererlab/ph_preference](https://github.com/fiererlab/ph_preference)

### Matching ASVs to GTDB 
Download genome/16S rDNA SSU database
```sh
wget https://data.gtdb.ecogenomic.org/releases/release207/207.0/genomic_files_reps/bac120_ssu_reps_r207.tar.gz 

tar -xzvf bac120_ssu_reps_r207.tar.gz
```
### Transform database to a vsearch reference database
```sh

vsearch --makeudb_usearch bac120_ssu_reps_r207.fna -output bac120_ssu_reps_r207.udb
```

## 1. Align the ASVs representative sequences to the GTDB reference database
```sh
thread=50
db=/public/home/2022122/chenhuilong/ph_preference/data/bac120_ssu_reps_r207.udb
protin=/public/home/2022122/xugang/database/gtdb3/protein_faa_reps/bacteria_processed
#node=Fnode2
#node=Fnode1
node=Cnode
node=Cnode2
#node=Gnode
counter=0
output=`pwd`/data

```
```sh

vsmap(){
name1=$1
name2=$2
((counter++))
file=''
[[ -d $output/log ]] || mkdir -p $output/log
echo -e "#!/bin/bash
#SBATCH -o ${output}/log/${name1}.%j.out
#SBATCH -e ${output}/log/${name1}.%j.error
#SBATCH --partition=${node}
#SBATCH -J 1${name1}
#SBATCH -N 1
#SBATCH -n ${thread}
echo date
source /public/home/2022122/.bashrc
vsearch --usearch_global data/${name1} --db ${db} --strand both --notrunclabels --iddef 0 --id 0.99 --maxrejects 100 --maxaccepts 100 --blast6out data/${name2} --threads ${thread}
" > a1.vsmapf.${counter}.${name1}.sh
}

vsmap pH_preferences_ASVs_PAN_ID.607.fasta PAN_607_aligned_ssu.tsv

```
aligned_ssu.tsv结果如下，即blast output format 6 file：

## 2. select the aligment bewteen ASV and reference genomes. 
使用“python according_to_vsearch_blast6out_result_extract_the_single_match_genome.py”
脚本（optional—）根据PAN_607_aligned_ssu.tsv得到大于等于99.6%的结果并提出ASV与细菌基因
组的唯一对应ID（asv_vs._genome_id.txt）  

```sh
#cd data
#python ../script/according_to_vsearch_blast6out_result_extract_the_single_match_genome.py -i PAN_607_aligned_ssu.tsv -o1 asv_genome_id_unique_match_ID.txt -o2 result
#cut -f 1,2 asv_genome_id_unique_match_ID.txt 
#cd ..
perl script/extract.96.pl data/PAN_607_aligned_ssu.tsv data/asv_genome_id_unique_match_ID.txt 


```
反之，如果B列都有唯一匹配的基因组序列：

就直接复制A和B列即可。
文件内容如下：
```sh
cat asv_vs._genome_id.txt

ASV_113 GB_GCA_003222395.1
ASV_1222 RS_GCF_000239795.1
ASV_1254 RS_GCF_012641395.1
... ...
ASV_998 RS_GCF_001542915.1
```


## 3. Extract proteins sequences from GTDB database files.
使用“batch_according_to_match_id_file_extract_genome_multisequence.py”脚本根据上一步得到的asv_vs._genome_id.txt文件，从已处理好的集群中的细菌基因组数据库中，批量萃取到ASV对应的细菌基因组的全蛋白组序列，并自动生成在genome_extract_result文件夹中。如下：


```sh

python script/batch_according_to_match_id_file_extract_genome_multisequence.py -i data/asv_vs._genome_id.txt -d ${protein} -o data/genome_extract_result

```
## 4. Annotation protion function with hmmscan.
对提取出来的目标蛋白组进行基因类型注释
conda activate pfam_annotation（我在集群中建了一个conda镜像（里面安装配置好HMMER软件
并配置好Pfam数据库））
使用“batch_run_hmmscan.py”脚本根据上一步得到的全蛋白组序列，批量自动进行hmmscan的程序调
用和全蛋白组的基因注释，并自动将基因注释结果生成在目标文件夹中。
#hmmscan注释一个细菌基因组的时长大约1个小时，所以这步会很耗时。
```sh
conda activate pfam_annotation
python batch_run_hmmscan.py -i data/genome_extract_result -o data/hmmscanResult
conda deactivate
```
## 5. 
根据hmmscanResult文件夹中的结果，使用“batch_according_to_hmmResult_extract_all_gene_presence_or_absence_table-command_format.py“脚本批量提取细菌基因组全部基因类型的存在或缺失矩阵表。
```sh
python batch_according_to_hmmResult_extract_all_gene_presence_or_absence_table-command_format.py -i  data/asv_vs._genome_id.txt -m data/hmmscanResult -o data/all_gene_presence_absence_table_result
```
