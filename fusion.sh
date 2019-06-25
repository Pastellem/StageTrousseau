 #!/bin/bash +v

#INPUT Variables
WGS_un=$1
WGS_deux=$2
WGS_CNV=$3
WES_SNP=$4
WES_CNV=$5
echo "Remove Id annotation" 
#cat $1 |awk -F "\t" '{print $1";"$2";"$4";"$5";"$6";"$7";"$8";"$9";"$10}'> WGS_un
#cat $2 |awk -F "\t" '{print $1";"$2";"$4";"$5";"$6";"$7";"$8";"$9";"$10}'> WGS_deux
#cat $3 |awk -F "\t" '{print $1";"$2";"$4";"$5";"$6";"$7";"$8";"$9";"$10}'> WGS_CNV
#cat $4 |awk -F "\t" '{print $1";"$2";"$4";"$5";"$6";"$7";"$8";"$9";"$10}'> WES_SNP
#cat $5 |awk -F "\t" '{print $1";"$2";"$4";"$5";"$6";"$7";"$8";"$9";"$10}'> WES_CNV

echo "Fusion de WGS 1 et 2"
#detection des mauvaise ligne
#grep -v "^#" WGS_un > tmp # on retire les ligne meta
#grep -v "^chr" tmp > tmpMauvais
#grep "^chr" WGS_un > tmpBon
#sed -i "s/^.*/chr&/g" tmpMauvais > tmpCorrige
#cat tmpCorrige tmpBon > tmpWGS1.vcf

#grep -v "^#" WGS_deux > tmp # on retire les ligne meta
#grep -v "^chr" tmp > tmpMauvais
#grep "^chr" WGS_deux > tmpBon
#sed -i "s/^/chr&/g" tmpMauvais > tmpCorrige
#cat tmpCorrige tmpBon > tmpWGS2.vcf
#echo "Nouveau WGS_SNP"
#cat tmpWGS1.vcf tmpWGS2.vcf > tmpWGS_SNP
#cat tmpWGS_SNP WGS_CNV |grep -v "^#" > tmpWGS


echo "Cat des WES"
#cat WES_SNP WES_CNV |grep -v "^#" > tmpWES # on retire les ligne meta


#cat tmpWGS|awk -F ";" '{print $1";"$2";"$3";"$4}' > tmp_Sha_WGS
#cat tmpWES|awk -F ";" '{print $1";"$2";"$3";"$4}' > tmp_Sha_WES

echo "Search Doublons in file SHA WGS vs WES"
#cat tmp_Sha_WGS tmp_Sha_WES | sort | uniq -d > tmp_Sha_doublons

#cat tmp_Sha_doublons tmp_Sha_WES | sort| uniq -u > tmpSHAUniqWES
#cat tmp_Sha_doublons tmp_Sha_WGS | sort| uniq -u > tmpSHAUniqWGS

#echo "Search Uniq in file WGS vs Doublon"
#grep -F -f tmpSHAUniqWGS tmpWGS > tmpuniqWGS

echo "Search Uniq in file Doublon vs WES"
#grep -F -f tmpSHAUniqWES tmpWES > tmpuniqWES

#grep -F -f tmp_Sha_doublons tmpWES > tmpDoublonWES
#grep -F -f tmp_Sha_doublons tmpWGS > tmpDoublonWGS
cat tmpDoublonWES tmpDoublonWGS| sort | uniq -u > tmpdoublon

echo "Tag absence/presence WGS or WES or both"
sed -e "s/$/;Type=WGS-WES/g" tmpdoublon > tmpdoublons2
sed -e "s/$/;Type=WGS-0/g" tmpuniqWGS > tmpuniqWGS2
sed -e "s/$/;Type=0-WES/g" tmpuniqWES > tmpuniqWES2

echo "Cat final form"
cat tmpdoublons2 tmpuniqWGS2 tmpuniqWES2 > CRO6502.vcf

echo "cleaning tempory file"
#rm tmp*
