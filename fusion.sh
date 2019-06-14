 #!/bin/bash +v

#INPUT Variables
WGS_SNP=$1
WGS_CNV=$2
WES_SNP=$3
WES_CNV=$4

echo "Cat des WGS"
cat $WGS_SNP $WGS_CNV > tmpWGS.vcf

echo "Cat des WES"
cat $WES_SNP $WES_CNV > tmpWES.vcf

echo "Search Doublons in file WGS vs WES"
cat tmpWGS.vcf tmpWES.vcf| sort -T .| uniq -d > tmpdoublons

echo "Search Doublons in file WGS vs Doublon"
cat tmpWGS.vcf tmpdoublons| sort -T .| uniq -u > tmpuniqWGS

echo "Search Doublons in file Doublon vs WES"
cat tmpWES.vcf tmpdoublons| sort -T .| uniq -u > tmpuniqWES

echo "Tag absence/presence WGS or WES or both"
sed -e "s/$/\tType=WGS-WES/g" tmpdoublons > tmpdoublons2
sed -e "s/$/\tType=WGS-0/g" tmpuniqWGS > tmpuniqWGS2
sed -e "s/$/\tType=0-WES/g" tmpuniqWES > tmpuniqWES2

echo "Cat final form"
cat tmpdoublons2 tmpuniqWGS2 tmpuniqWES2|sort -T .|uniq -u > fichier_name.vcf

echo "cleaning tempory file"
rm tmp*
