 #!/bin/bash +v

#INPUT Variables
WGS_SNP=$1
WGS_CNV=$2
WES_SNP=$3
WES_CNV=$4

echo "Cat des WGS"
cat $WGS_SNP $WGS_CNV |grep -v "^#" > tmpWGS.vcf

echo "Cat des WES"
cat $WES_SNP $WES_CNV |grep -v "#" > tmpWES.vcf


cat tmpWGS.vcf|awk -F "\t" '{print $1"_"$2"_"$3"_"$4"_"$5}' > tmp_Sha_WGS
cat tmpWES.vcf|awk -F "\t" '{print $1"_"$2"_"$3"_"$4"_"$5}' > tmp_Sha_WES

echo "Search Doublons in file SHA WGS vs WES"
cat tmp_Sha_WGS tmp_Sha_WES | sort -T tmpSort | uniq -d > tmp_Sha_doublons

sed -i "s/\_/\t/g" tmp_Sha_doublons
sed -i "s/\_/\t/g" tmp_Sha_WES
sed -i "s/\_/\t/g" tmp_Sha_WGS

echo "Search Uniq in file WGS vs Doublon"
grep -v -F -f tmp_Sha_doublons tmpWGS.vcf | sort -T tmpSort | uniq -u > tmpuniqWGS

echo "Search Uniq in file Doublon vs WES"
grep -v -F -f tmp_Sha_doublons tmpWES.vcf | sort -T tmpSort| uniq -u > tmpuniqWES

grep -F -f tmp_Sha_doublons tmpWES.vcf > tmDoublonWES
grep -F -f tmp_Sha_doublons tmpWGS.vcf > tmpDoublouWGS
cat tmDoublonWES tmpDoublouWGS > tmpdoublon

echo "Tag absence/presence WGS or WES or both"
sed -e "s/$/\tType=WGS-WES/g" tmpdoublon > tmpdoublons2
sed -e "s/$/\tType=WGS-0/g" tmpuniqWGS > tmpuniqWGS2
sed -e "s/$/\tType=0-WES/g" tmpuniqWES > tmpuniqWES2

echo "Cat final form"
cat tmpdoublons2 tmpuniqWGS2 tmpuniqWES2 > fichier_name.vcf

echo "cleaning tempory file"
rm tmp*
